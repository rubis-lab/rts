from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.gen.gen import Gen

import random
import math


class Egen(Gen):
    def __init__(self, **kwargs):
        super(type(self), self).__init__(**kwargs)
        self.tot_util = kwargs.get('tot_util', 1.0)
        self.ts = TaskSet()
        self.last_id = -1

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
        info = 'Generator - egen\n' + \
            super(type(self), self).__str__() + '\n' + \
            'tot_util = ' + str(self.tot_util)
        return info

    def create_new_task_set(self, t):
        self.ts.clear()

        if t.utilization() <= self.tot_util:
            self.last_id = 0
            t.id = self.last_id
            self.ts.append(t)
            return self.ts
        else:
            return -1

    def next_task_set(self):
        # try append task to existing task set
        t = self.next_task()
        if self.ts.tot_util() + t.utilization() >= self.tot_util:
            return self.create_new_task_set(t)

        # append task to existing task set
        self.last_id += 1
        t.id = self.last_id
        self.ts.append(t)

        return self.ts
