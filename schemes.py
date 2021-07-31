import time

from pydantic import BaseModel


class LearningSession(BaseModel):
    id: str = None
    learningLanguage: str = None
    fromLanguage: str = None
    type: str = None
    challenges: list = None
    adaptiveChallenges: list = None
    adaptiveInterleavedChallenges: dict = None
    metadata: dict = None
    trackingProperties: dict = None
    beginner: bool = None
    skillId: str = None
    sessionStartExperiments: list = None
    lessonIndex: int = None
    levelIndex: int = None
    levelSessionIndex: int = None
    preSessionScreens: list = None
    challengeTimeTakenCutoff: int = None
    explanations: dict = None
    progressUpdates: list = None

    disable_bonus_points: bool = False
    startTime: int = int(time.time())
    failed: bool = False
    heartsLeft: int = 0
    max_in_lesson_streak: int = None
    endTime: int = startTime


class Skill(BaseModel):
    id: str = None
    name: str = None
    levels: int = None
    lessons: int = None
    finishedLevels: int = None
    finishedLessons: int = None
