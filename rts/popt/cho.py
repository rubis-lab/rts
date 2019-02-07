from rts.popt.popt import Popt
from rts.sched.sched import Sched
from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pts import ParaTaskSet
from rts.sched.bcl_naive import BCL_Naive
from rts.op import tsutil


class Cho(Popt):
    'Cho 2019'

    def __init__(self, **kwargs):
        self.max_opt = kwargs.get('max_option', 1)
        self.sched = kwargs.get('sched', Sched())
        return

    def __del__(self):
        return

    def __str__(self):
        info = ''
        return info

    def create_inter_vs_popt_table(self, pts):
        self.ip_table = []
        n_task = len(pts.base_ts)
        for i in range(n_task):
            self.ip_table.append([])
            for j in range(self.max_opt):
                # thread set of task i, option j + 1
                thrs_i_oj = pts.pt_list[i][j + 1]

                # Minimum laxity (D - C) among thread set
                lax = []
                for k in range(len(thrs_i_oj)):
                    lax.append(thrs_i_oj[k].deadline - thrs_i_oj[k].exec_time)

                print('thrs_i list')
                print(i)
                print(thrs_i_oj)
                print('lax list')
                print(lax)
                print('min lax value')
                print(min(lax))
                print('min lax idx')
                print(lax.index(min(lax)))
                print('corresponding thr')
                print(thrs_i_oj[lax.index(min(lax))])

                self.ip_table[i].append(min(lax))
        return

    def is_schedulable(self, pts):
        # Create interference vs parallel option table for every task
        self.create_inter_vs_popt_table(pts)
        print('ip_table')
        print(self.ip_table)

        # Initial - all tasks at lowest parallelization
        pts.popt_strategy = 'single'
        pts.serialize_pts()

        n_task = len(pts.base_ts)
        for i in range(n_task):
            pass

        """
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
        """
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
        'max_option': 4,
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
        'max_option': 4,
        'sched':bcl_naive,
    }
    exhaustive = Cho(**popt_param)

    ss = exhaustive.is_schedulable(pts)
    print('Exhaustive test result:')
    print(ss)
