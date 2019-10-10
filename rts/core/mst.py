from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pt import ParaTask
from rts.op import para
from rts.op import tsutil
import random


class MultiSegmentTask(object):
    """
    'Multi Segment Task'
    """
    cnt = 0

    def __init__(self, **kwargs):
        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)

        # parallelizer info
        self.max_opt = kwargs.get('max_option', 1)
        self.overhead = kwargs.get('overhead', 0.0)
        self.variance = kwargs.get('variance', 0.0)

        # base para task set info
        # tmp_ts: default task set with a single dummy task.
        tmp_ts = TaskSet()
        tmp_ts.append(Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))
        self.base_ts = kwargs.get('base_ts', tmp_ts)
        self.pt_list = []

        if kwargs.get('custom', 'False') == 'True':
            self.pt_list = kwargs.get('pt_list', [[]])
        else:
            self.populate_pt_list()

        # create a list of task sets according to selected option.
        # defaults to single thread for each pt
        self.popt_strategy = kwargs.get('popt_strategy', 'single')
        self.popt_list = kwargs.get('popt_list', [1 for _ in range(len(self.pt_list))])

        self.ts_list = []
        self.update_ts_list()
        return

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        info = 'id: ' + str(self.id) + '\n' + \
            'max_option: ' + str(self.max_opt) + '\n' + \
            'popt_strategy: ' + self.popt_strategy + '\n' + \
            'num_segments: ' + str(len(self)) + '\n' + \
            'tot_util: ' + str(self.tot_util()) + '\n\n' + \
            'generated: \n'
        for i, ts in enumerate(self.ts_list):
            info += 'segment ' + str(i + 1) + '\n' + \
                str(ts) + '\n'
        return info

    def __len__(self):
        return len(self.ts_list)

    def __getitem__(self, idx):
        return self.ts_list[idx]

    def __setitem__(self, idx, thr):
        self.ts_list[idx] = thr
        return

    def __iter__(self):
        return iter(self.ts_list)

    def clear(self):
        del self.ts_list[:]
        del self.pt_list[:]
        return

    def populate_pt_list(self):
        for t in self.base_ts:
            para_task_param = {
                'base_task': t,
                'max_option': self.max_opt,
                'overhead': self.overhead,
                'variance': self.variance,
            }
            pt = ParaTask(**para_task_param)
            self.pt_list.append(pt)
        return

    def update_ts_list(self):
        if self.popt_strategy == 'single':
            self.ts_list = para.parallelize_multiseg_single(self.pt_list)
        elif self.popt_strategy == 'max':
            self.ts_list = para.parallelize_multiseg_max(self.pt_list, **{'max_option': self.max_opt})
        elif self.popt_strategy == 'random':
            del self.popt_list[:]
            for i in range(len(self.base_ts)):
                self.popt_list.append(random.randint(1, self.max_opt))
            self.ts_list = para.parallelize_multiseg_custom(self.pt_list, self.popt_list)
        elif self.popt_strategy == 'custom':
            self.ts_list = para.parallelize_multiseg_custom(self.pt_list, self.popt_list)
        else:
            raise Exception('Parallelization strategy not defined')

    def tot_util(self):
        sum_util = 0.0
        for ts in self.ts_list:
            sum_util += tsutil.sum_utilization(ts)
        return sum_util
