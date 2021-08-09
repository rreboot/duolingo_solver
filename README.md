# Duolingo solver
Automatic solver for Duolingo. (**Description made with google translate**)

## Overview

Duolingo solver allows you to automatically solve skills from your course.

Example:
```python
from solver import DuolingoSolver

solver = DuolingoSolver(username='rReBoOT',
                        token='some token',
                        sleep_time=1)
solver.solve_all()
```
Result:
```text
Solving skill: Еда
Returned session id: t5u16SASm8tuVtnZ
Challenge solution: Конечно, моя дочь любит американскую еду.. Sleeping 1 seconds.
Challenge solution: I am not hungry.. Sleeping 1 seconds.
Challenge solution: Нет, Света не голодная.. Sleeping 1 seconds.
Challenge solution: Yes, my wife likes American food.. Sleeping 1 seconds.
Challenge solution: Русская еда острая?. Sleeping 1 seconds.
Challenge solution: Of course my daughter likes American food.. Sleeping 1 seconds.
Challenge solution: Конечно, я люблю русскую еду, я из России!. Sleeping 1 seconds.
Challenge solution: I like Russian food and red wine.. Sleeping 1 seconds.
Challenge solution: Бен такой голодный.. Sleeping 1 seconds.
Challenge solution: I am so hungry.. Sleeping 1 seconds.
Challenge solution: Извините, этот гамбургер острый?. Sleeping 1 seconds.
Challenge solution: Maria likes American food, she is from Boston!. Sleeping 1 seconds.
Challenge solution: Я такая голодная.. Sleeping 1 seconds.
Challenge solution: Is American food spicy?. Sleeping 1 seconds.
Challenge solution: Я люблю русскую еду и красное вино.. Sleeping 1 seconds.
Challenge solution: Is Russian food spicy?. Sleeping 1 seconds.
Challenge solution: Excuse me, is this hamburger spicy?. Sleeping 1 seconds.
OK! Solved!
Lesson: 1. Level: 1
Returned session id: gIbdeGLKpa2O3SOu
Challenge solution: Бен, ты любишь острую еду?. Sleeping 1 seconds.
Challenge solution: Do you like Russian food?. Sleeping 1 seconds.
...
```