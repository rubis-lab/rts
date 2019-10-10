from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.gen.gen import Gen

from rts.core.mst import MultiSegmentTask
from rts.core.msts import MultiSegmentTaskSet

import random
import math


class MSgen(Gen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tot_util = kwargs.get('tot_util', 1.0)
        self.msts = MultiSegmentTaskSet()
        self.utilization_overflow = kwargs.get('util_over', True)
        self.deadline_scale = kwargs.get('deadline_scale', 1.0)
        self.max_mst_util = kwargs.get('max_mst_util', 1.0)
        self.min_seg_size = kwargs.get('min_seg_size',  10)
        self.max_seg_size = kwargs.get('max_seg_size', 20)
        self.max_option = kwargs.get('max_option', 1)

    def next_mst(self):
        base_t = self.next_task()

        # create random chunks using original execution time
        e_tot = base_t.exec_time
        e_list = []
        while e_tot >= self.min_seg_size:
            e_tmp = random.randint(self.min_seg_size, self.max_seg_size)
            e_tmp = min(e_tot, e_tmp)  # e should not increase
            e_list.append(e_tmp)
            e_tot -= e_tmp
        random.shuffle(e_list)

        # make tasks using the chunks, create task set
        ts = TaskSet()
        for e in e_list:
            task_param = {
                'period': base_t.period,
                'exec_time': e,
                'deadline': base_t.deadline,
            }
            t = Task(**task_param)
            ts.append(t)

        # create mst based on ts
        ms = MultiSegmentTask(**{
            'base_ts': ts,
            'max_option': self.max_option,
            'popt_strategy': 'single'
        })
        return ms

    def next_task(self):
        period = random.randint(self.min_period, self.max_period)
        exec_time = random.randint(self.min_exec_time, self.max_exec_time)

        # prevents tasks with utilization > 1.0
        if not self.utilization_overflow:
            while exec_time > period + 0.1:
                period = random.randint(self.min_period, self.max_period)
                exec_time = random.randint(self.min_exec_time, self.max_exec_time)

        if self.implicit_deadline:
            deadline = period
        else:
            if self.constrained_deadline:
                deadline = random.randint(self.min_deadline, period)
            else:
                deadline = random.randint(self.min_deadline, self.max_deadline)

        task_param = {
            'period': period,
            'exec_time': exec_time,
            'deadline': deadline * self.deadline_scale,
        }

        t = Task(**task_param)
        return t

    def __str__(self):
        info = 'Generator - mstgen\n' + \
            super(type(self), self).__str__() + '\n' + \
            'tot_util = ' + str(self.tot_util) + '\n' + \
            'util_over = ' + str(self.utilization_overflow) + '\n' + \
            'implicit_deadline = ' + str(self.implicit_deadline) + '\n' + \
            'constrained_deadline = ' + str(self.constrained_deadline) + '\n' + \
            'min_seg_size = ' + str(self.min_seg_size) + '\n' + \
            'max_seg_size = ' + str(self.max_seg_size) + '\n' + \
            'max_option = ' + str(self.max_option)
        return info

    def create_new_mst_set(self, mst):
        self.msts.clear()

        if mst.tot_util() <= self.tot_util:
            self.msts.append(mst)
            return self.msts
        else:
            raise Exception('Cannot create new task set, tried utilization: ' + mst.tot_util())

    def next_mst_set(self):
        # try to append a task to the existing mst set
        mst = self.next_mst()
        if self.msts.tot_util() + mst.tot_util() >= self.tot_util:
            return self.create_new_mst_set(mst)

        # append task to existing task set
        self.msts.append(mst)

        return self.msts


if __name__ == '__main__':

    gen_param = {
        'min_exec_time': 30,
        'max_exec_time': 100,
        'min_period': 60,
        'max_period': 200,
        'min_deadline': 40,
        'max_deadline': 200,
        'tot_util': 4.0,
        'util_over': True,
        'implicit_deadline': False,
        'constrained_deadline': True,
        'min_seg_size': 10,
        'max_seg_size': 30,
        'max_option': 4
    }
    msg = MSgen(**gen_param)
    msts = msg.next_mst_set()
    print(msts)

    print(msg)
