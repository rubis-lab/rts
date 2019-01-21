from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.gen.gen import Gen

import random
import math


class Ugen(Gen):
    def __init__(self, **kwargs):
        super(type(self), self).__init__(**kwargs)
        self.tot_util = kwargs.get('tot_util', 1.0)

    def next_task(self, **kwargs):
        period = random.randint(self.min_period, self.max_period)
        exec_time = random.randint(self.min_exec_time, self.max_exec_time)
        deadline = period  # implicit deadline
        task_param = {
            'period': period,
            'exec_time': exec_time,
            'deadline': deadline,
        }

        t = Task(**task_param)
        return t

    def __str__(self):
        info = 'Generator - ugen\n' + \
            super(type(self), self).__str__() + '\n' + \
            'tot_util = ' + str(self.tot_util)
        return info

    def next_task_set(self):
        ts = TaskSet()
        for i in range(self.num_task):
            t = self.next_task()
            t.id = i
            if ts.tot_util() + t.utilization() >= self.tot_util:
                break
            ts.append(t)
        return ts
