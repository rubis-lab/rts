from rts.popt.popt import Popt
from rts.sched.sched import Sched
from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pts import ParaTaskSet
from rts.sched.bcl_naive import BCL_Naive

class Exhaustive(Popt):
    'Exhaustive search'

    def __init__(self, **kwargs):
        self.max_opt = kwargs.get('max_option', 1)
        self.sched = kwargs.get('sched', Sched())
        return

    def __del__(self):
        return

    def __str__(self):
        info = ''
        return info

    def conv_num_base(self, n, b, idx):
        if n == 0:
            return idx
        i = 0
        while n:
            idx[i] = int(n % b)
            i += 1
            n //= b
        return idx

    def is_schedulable(self, pts):
        # number of possible cases: max_opt ^ n_task
        n_task = len(pts.base_ts)
        for i in range(self.max_opt ** n_task):
            #print('i')
            #print(i)
            idx = [0 for j in range(n_task)]
            #print('idx: ')
            self.conv_num_base(i, self.max_opt, idx)
            #print(idx)

            # set parallel option
            for j in range(n_task):
                pts.popt_list[j] = idx[j] + 1
            pts.serialize_pts()
            #print(pts)

            # check schedulability
            if self.sched.is_schedulable(pts):
                #print('True')
                return True
            #print('False')

        return False

    def get_opt_popt(self, pts):
        pass


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
        'max_option': 2,
        'overhead': 0.0,
        'variance': 0.3,
        'popt_strategy': 'custom',
        'popt_list': [1, 1],
    }

    pts = ParaTaskSet(**pts_param)
    print(pts)

    sched_param = {
        'num_core': 1.0,
    }
    bcl_naive = BCL_Naive(**sched_param)

    popt_param = {
        'max_option': 2,
        'sched':bcl_naive,
    }
    exhaustive = Exhaustive(**popt_param)

    ss = exhaustive.is_schedulable(pts)
    print('Exhaustive test result:')
    print(ss)
