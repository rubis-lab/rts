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

        # task like property
        self.exec_time = -1 # sum of all exec_times
        self.crit_exec_time = -1 # sum of largest exec_times
        self.deadline = self.base_ts[0].deadline
        self.period = self.base_ts[0].period

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

        # update longest exec_time
        self.update_exec_time()

    def update_exec_time(self):
        self.crit_exec_time = 0.0
        self.exec_time = 0.0
        for ts in self.ts_list:
            self.crit_exec_time += ts[0].exec_time  # sum of largest exec_time (longest path)
            for t in ts:
                self.exec_time += t.exec_time  # sum of all exec_time

    def tot_util(self):
        return self.exec_time / self.period


if __name__ == '__main__':
    t1 = Task(**{
        'exec_time': 20,
        'deadline': 30,
        'period': 40
    })
    t2 = Task(**{
        'exec_time': 40,
        'deadline': 60,
        'period': 80
    })
    ts = TaskSet()
    ts.append(t1)
    ts.append(t2)

    ms = MultiSegmentTask(**{
        'base_ts': ts,
        'max_option': 4,
        'popt_strategy': 'max'
    })

    print(ms)
    print(ms.crit_exec_time)
    print(ms.exec_time)
    print(ms.tot_util())
