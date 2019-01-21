from rts.core.task import Task
from rts.core.ts import TaskSet

import random


class Gen(object):
    'Basic generator class'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed', 0)
        random.seed(self.seed)
        self.num_task = kwargs.get('num_task', 0)
        self.min_exec_time = kwargs.get('min_exec_time', 0)
        self.max_exec_time = kwargs.get('max_exec_time', 0)
        self.min_deadline = kwargs.get('min_deadline', 0)
        self.max_deadline = kwargs.get('max_deadline', 0)
        self.min_period = kwargs.get('min_period', 0)
        self.max_period = kwargs.get('max_period', 0)
        return

    def __del__(self):
        return

    def __str__(self):
        info = 'num_task = ' + str(self.num_task) + '\n' + \
            'min_exec_time = ' + str(self.min_exec_time) + '\n' + \
            'max_exec_time = ' + str(self.max_exec_time) + '\n' + \
            'min_deadline = ' + str(self.min_deadline) + '\n' + \
            'max_deadline = ' + str(self.max_deadline) + '\n' + \
            'min_period = ' + str(self.min_period) + '\n' + \
            'max_period = ' + str(self.max_period)
        return info

    def next_task(self, **kwargs):
        task_param = {
            'exec_time': random.randint(
                self.min_exec_time, self.max_exec_time),
            'deadline': random.randint(
                self.min_deadline, self.max_deadline),
            'period': random.randint(
                self.min_period, self.max_period),
        }

        t = Task(**task_param)
        return t

    def next_task_set(self):
        ts = TaskSet()
        for i in range(self.num_task):
            t = self.next_task()
            ts.append(t)
        return ts


if __name__ == '__main__':
    gen_param = {
        'num_task': 10,
        'min_exec_time': 0,
        'max_exec_time': 10,
        'min_deadline': 0,
        'max_deadline': 10,
        'min_period': 0,
        'max_period': 10,
    }
    g = Gen(**gen_param)
    ts = g.next_task_set()

    for t in ts:
        print(t)

    print(g)
