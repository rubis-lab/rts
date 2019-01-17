from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.gen.gen import Gen

import random
import math

class Ugen(Gen):
    def __init__(self, **kwargs):
        super(type(self), self).__init__(**kwargs)
        self.tot_util = kwargs.get('tot_util', 1.0)

    def __str__(self):
        info = super(type(self), self).__str__()
        info += 'tot_util = ' + str(self.tot_util) + '\n'
        return info

    def next_task(self, **kwargs):
        cand_util = kwargs.get('cand_util', 0.0)

        period = random.randint(self.min_period, self.max_period)
        exec_time = math.floor(period * cand_util)
        deadline = period  # implicit deadline
        task_param = {
            'period': period,
            'exec_time': exec_time,
            'deadline': deadline,
        }

        t = Task(**task_param)
        return t

    def next_task_set(self):
        divided_util = self.unifast_divide(self.num_task, self.tot_util)

        ts = TaskSet()
        for i in range(self.num_task):
            t = self.next_task(cand_util=divided_util[i])
            t.id = i
            ts.append(t)
        return ts