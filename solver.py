import time
from itertools import chain
from typing import List

import requests

from schemes import Skill, LearningSession


class DuolingoSolver:
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    token: str = None
    username: str = None
    user_id: int = None
    sleep_time: float = None
    solved_skills: list = []

    def __init__(self, token: str, username: str, sleep_time: float = 3):
        self.token = token
        self.username = username
        self.sleep_time = sleep_time
        self._init_headers()
        self.user_id = self._get_user_id()

    def _init_headers(self):
        self.headers['authorization'] = f'Bearer {self.token}'

    def _get_user_id(self):
        """ Get FIRST user id.

        """
        url = f'https://www.duolingo.com/2017-06-30/users' \
              f'?username={self.username}&fields=users%7Bid%7D'
        response = requests.get(url=url, headers=self.headers).json()

        return response['users'][0]['id']

    def get_skills(self, only_unsolved=True) -> List[Skill]:
        """ Return list of skills.

        Parameters
        ----------
        only_unsolved : bool
            Add to list only unsolved skills.

        Returns
        -------
        List[Skill]

        """
        url = f'https://www.duolingo.com/2017-06-30/users/{self.user_id}' \
              f'?fields=currentCourse%7Bskills%7D'
        response = requests.get(url=url, headers=self.headers).json()

        skills_list = []
        current_course = response['currentCourse']
        skills = current_course['skills']

        for skill in chain.from_iterable(skills):
            levels = skill['levels']
            finished_levels = skill['finishedLevels']
            lessons = skill['lessons']
            finished_lessons = skill['finishedLessons']

            if only_unsolved:
                if levels == finished_levels and lessons == finished_lessons:
                    continue

            skills_list.append(
                Skill(id=skill['id'],
                      name=skill['name'],
                      levels=levels,
                      lessons=lessons,
                      finishedLevels=finished_levels,
                      finishedLessons=finished_lessons)
            )

        return skills_list

    def solve_skill(self, skill: Skill):
        """ Complete solve one skill.

        """
        print(f'Solving skill: {skill.name}')

        while True:
            if skill.finishedLevels == skill.levels \
                    and skill.finishedLessons == skill.lessons:
                break

            session = self._get_session(skill_id=skill.id,
                                        finished_levels=skill.finishedLevels,
                                        finished_lessons=skill.finishedLessons)
            self._solve_session(session)

            if skill.finishedLessons < skill.lessons:
                skill.finishedLessons += 1
            else:
                skill.finishedLessons = 0
                skill.finishedLevels += 1

            print(f'Lesson: {skill.finishedLessons}. Level: {skill.finishedLevels}')

        print(f'Skill [{skill.name}] - completed.')

    def solve_first(self):
        """ Solve first unsolved skill.

        """
        skills = self.get_skills()
        first_unsolved = skills[0]
        self.solve_skill(first_unsolved)

    def solve_all(self):
        """ Solve all skills.

        """
        skills = self.get_skills()

        for skill in skills:
            try:
                self.solve_skill(skill)
                self.solved_skills.append(skill.name)
            except Exception as e:
                print(f'Solved skills: {self.solved_skills}')
                raise e
            except KeyboardInterrupt:
                print(f'Solved skills: {self.solved_skills}. Stopped.')
                exit(0)

    def _get_session(
            self, skill_id: str, finished_levels: int, finished_lessons: int
    ) -> LearningSession:
        """ Get learning session.

        Parameters
        ----------
        skill_id : str
        finished_levels : int
        finished_lessons : int

        Returns
        -------
        session : LearningSession

        """
        url = 'https://www.duolingo.com/2017-06-30/sessions'
        payload = {'challengeTypes': ['characterIntro',
                                      'characterMatch',
                                      'characterSelect',
                                      'characterTrace',
                                      # 'completeReverseTranslation',
                                      'definition',
                                      'dialogue',
                                      # 'form',
                                      'freeResponse',
                                      'gapFill',
                                      # 'judge',
                                      # 'listen',
                                      'name',
                                      # 'listenComprehension',
                                      # 'listenTap',
                                      'readComprehension',
                                      # 'select',
                                      # 'selectPronunciation',
                                      # 'selectTranscription',
                                      'tapCloze',
                                      'tapClozeTable',
                                      'tapComplete',
                                      'tapCompleteTable',
                                      'tapDescribe',
                                      'translate',
                                      'typeCloze',
                                      'typeClozeTable',
                                      'typeCompleteTable'],
                   'fromLanguage': 'ru',
                   'juicy': True,
                   'learningLanguage': 'en',
                   'smartTipsVersion': 2,
                   'levelIndex': finished_levels,
                   'levelSessionIndex': finished_lessons,
                   'showPreLessonTipSplash': False,
                   'skillId': skill_id,
                   'type': 'LESSON',
                   'speakIneligibleReasons': 'permission_disabled'}

        response = requests.post(url=url, headers=self.headers,
                                 json=payload).json()
        session = LearningSession(**response)
        session.max_in_lesson_streak = len(session.challenges)

        print(f'Returned session id: {session.id}')

        return session

    def _solve_session(self, session: LearningSession) -> None:
        """ Solve session lessions.

        Parameters
        ----------
        session : dict

        """
        url = f'https://www.duolingo.com/2017-06-30/sessions/{session.id}'

        for challenge in session.challenges:
            if challenge.get('grader'):
                del challenge['grader']
            challenge['correct'] = True
            correct_solution = challenge['correctSolutions'][0]
            challenge['closestSolution'] = correct_solution
            challenge['guess'] = correct_solution
            challenge['timeTaken'] = self.sleep_time * 1000  # time in milliseconds

            print(f'Challenge solution: {correct_solution}. '
                  f'Sleeping {self.sleep_time} seconds.')
            time.sleep(self.sleep_time)
            session.endTime += challenge['timeTaken']

        # Add 2 sec to endTime
        session.endTime += 2000

        response = requests.put(url=url, headers=self.headers, json=session.dict())

        if response.status_code != 200:
            print(f'Something wrong. Response: {response.text}')
        else:
            print('OK! Solved!')
