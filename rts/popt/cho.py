from rts.popt.popt import Popt
from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pts import ParaTaskSet
from rts.op import tsutil
import math

class Cho(Popt):
    'Cho 2019'

    def __init__(self, **kwargs):
        self.max_opt = kwargs.get('max_option', 1)
        self.num_core = float(kwargs.get('num_core', 1.0))
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
            # option 0 will not be used
            self.ip_table.append([-1.0])

            for j in range(self.max_opt):
                # thread set of task i, option j + 1
                thrs_i_oj = pts.pt_list[i][j + 1]

                # Minimum laxity (D - C) among thread set
                lax = []
                for k in range(len(thrs_i_oj)):
                    lax.append(thrs_i_oj[k].deadline - thrs_i_oj[k].exec_time)
                """
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
                """
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
        n_task = len(pts.pt_list)
        selected_opt = [1 for i in range(n_task)]

        # Iteration
        while True:
            """
            Calculate interference of other tasks.
            Only need to calculate once for each bask task,
            because worst case is when laxity is the least.
            Least laxity thread is the first thread,
            which has the largest execution time.
            """
            i_sum_list = []
            for i in range(n_task):
                base_thr = pts.pt_list[i][selected_opt[i]][0]
                i_sum = -base_thr.exec_time
                for j in range(len(pts)):
                    inter_thr = pts[j]
                    i_sum += tsutil.workload_in_interval_edf(inter_thr, base_thr.deadline)
                i_sum = math.floor(i_sum / self.num_core)
                print('i_sum')
                print(i_sum)
                i_sum_list.append(i_sum)

            """
            Find minimum possible option for each tasks.
            Compare with interference vs parallel option table created earlier.
            The option is always non decreasing.
            Increment option until it can tolerate calculated interference.
            """
            selected_opt_cpy = selected_opt[:]
            for i in range(n_task):
                base_pt = pts.pt_list[i]
                while selected_opt[i] < self.max_opt:
                    # floating value comparison... difference less than 0.1
                    if self.ip_table[i][selected_opt[i]] - i_sum_list[i] < 0.1:
                        selected_opt[i] += 1
                    else:
                        break
            print('selected_opt')
            print(selected_opt)

            # if no change needed, check convergence
            if selected_opt == selected_opt_cpy:
                """
                if any parallel option maxed out, but still its interference
                exceeds tolerence --> unschedulable
                else --> schedulable
                """
                for i in range(n_task):
                    # popt maxed out
                    if abs(selected_opt[i] - self.max_opt) < 0.1:
                        # interference over tolerence
                        if self.ip_table[i][selected_opt[i]] - i_sum_list[i] < 0.1:
                            return False
                # All tasks interference under tolerence
                return True

            print('----------------')

    def get_opt_popt(self, pts):
        pass


if __name__ == '__main__':
    task_param = {
        'exec_time': 35,
        'deadline': 60,
        'period': 60,
    }
    t1 = Task(**task_param)

    task_param = {
        'exec_time': 72,
        'deadline': 80,
        'period': 80,
    }
    t2 = Task(**task_param)

    ts = TaskSet()
    ts.append(t1)
    ts.append(t2)

    pts_param = {
        'base_ts': ts,
        'max_option': 4,
        'overhead': 0.0,
        'variance': 0.8,
        'popt_strategy': 'custom',
        'popt_list': [1, 1],
    }

    pts = ParaTaskSet(**pts_param)
    print(pts)

    popt_param = {
        'num_core': 2.0,
        'max_option': 4,
    }

    exhaustive = Cho(**popt_param)

    ss = exhaustive.is_schedulable(pts)
    print('Test result:')
    print(ss)
