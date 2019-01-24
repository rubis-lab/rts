from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pt import ParaTask
from rts.op import para

class ParaTaskSet(object):
    'Parallelizable Task Set'
    cnt = 0

    def __init__(self, **kwargs):
        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)
        self.max_opt = kwargs.get('max_option', 1)

        # parallelizer info
        self.overhead = kwargs.get('overhead', 0.0)
        self.variance = kwargs.get('variance', 0.0)

        # base task set info
        tmp_ts = TaskSet()
        tmp_ts.append(Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))
        self.base_ts = kwargs.get('base_ts', tmp_ts)
        self.pt_list = []

        self.populate_pt_list()

        # pts serialized according to selected option.
        # defaults to single thread for each pt in pts.
        self.popt = kwargs.get('popt', 'single')
        self.pts_serialized = TaskSet()
        self.serialize_pts(**{'popt': self.popt})
        return

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        info = 'id: ' + str(self.id) + '\n' + \
               'max_option: ' + str(self.max_opt) + '\n\n' + \
               'base_ts: ' + '\n' + str(self.base_ts) + '\n' + \
               'generated: \n' + str(self.pts_serialized)

        return info

    def __len__(self):
        return len(self.pts_serialized)

    def __getitem__(self, idx):
        return self.pts_serialized[idx]

    def __setitem__(self, idx, thr):
        self.pts_serialized[idx] = thr
        return

    def __iter__(self):
        return iter(self.pts_serialized)

    def clear(self):
        del self.pts_serialized[:]
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

    def serialize_pts(self, **kwargs):
        popt = kwargs.get('popt', 'single')

        if popt == 'single':
            self.pts_serialized.merge_ts(
                para.parallelize_pts_single(
                    self.pt_list
                )
            )
        elif popt == 'max':
            self.pts_serialized.merge_ts(
                para.parallelize_pts_max(
                    self.pt_list,
                    **{'max_option': self.max_opt}
                )
            )
        elif popt == 'random':
            self.pts_serialized.merge_ts(
                para.parallelize_pts_random(
                    self.pt_list,
                    **{'max_option': self.max_opt}
                )
            )
        else:
            raise Exception('Parallelization strategy not defined')


if __name__ == '__main__':
    task_param = {
        'exec_time': 4,
        'deadline': 10,
        'period': 10,
    }
    t1 = Task(**task_param)

    task_param = {
        'exec_time': 10,
        'deadline': 20,
        'period': 20,
    }
    t2 = Task(**task_param)

    ts = TaskSet()
    ts.append(t1)
    ts.append(t2)

    pts_param = {
        'base_ts': ts,
        'max_option': 4,
        'overhead': 0.0,
        'variance': 0.3,
        'popt': 'max',
    }

    pts = ParaTaskSet(**pts_param)
    print(pts)

