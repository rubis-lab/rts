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
        self.ip_table = []
        return

    def __del__(self):
        return

    def __str__(self):
        info = ''
        return info

    def create_inter_vs_popt_table(self, pts):
        del self.ip_table[:]
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
        # print('ip_table')
        # print(self.ip_table)

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
                i_sum = 0.0
                for j in range(len(pts)):
                    inter_thr = pts[j]
                    if inter_thr == base_thr:
                        continue
                    i_sum_tmp = tsutil.workload_in_interval_edf(inter_thr, base_thr.deadline)
                    # interference is limited to laxity of base thread
                    i_sum += max(0.0, min(i_sum_tmp, base_thr.deadline - base_thr.exec_time + 1.0))
                i_sum = math.floor(i_sum / self.num_core)
                # print('i_sum')
                # print(i_sum)
                i_sum_list.append(i_sum)

            """
            Find minimum possible option for each tasks.
            Compare with interference vs parallel option table created earlier.
            The option is always non decreasing.
            Increment option until it can tolerate calculated interference.
            """
            selected_opt_cpy = selected_opt[:]
            for i in range(n_task):
                while selected_opt[i] < self.max_opt:
                    # floating value comparison... difference less than 0.1
                    if i_sum_list[i] > self.ip_table[i][selected_opt[i]] + 0.1:
                        selected_opt[i] += 1
                    else:
                        break
            # print('selected_opt')
            # print(selected_opt)

            # if no change needed, check convergence
            if selected_opt == selected_opt_cpy:
                """
                if any parallel option maxed out, but still its interference
                exceeds tolerance --> unschedulable
                else --> schedulable
                """
                for i in range(n_task):
                    # popt maxed out
                    if selected_opt[i] >= self.max_opt:
                        # interference exceeds tolerance
                        if i_sum_list[i] > self.ip_table[i][selected_opt[i]] + 0.1:
                            return False
                # All tasks interference under tolerance
                return True

            # print('----------------')

    def is_schedulable_verbose(self, pts):
        # Create interference vs parallel option table for every task
        self.create_inter_vs_popt_table(pts)
        print('ip_table')
        print(self.ip_table)
        # print('ip_table')
        # print(self.ip_table)

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
                i_sum = 0.0
                for j in range(len(pts)):
                    inter_thr = pts[j]
                    if inter_thr == base_thr:
                        continue
                    i_sum_tmp = tsutil.workload_in_interval_edf(inter_thr, base_thr.deadline)
                    # interference is limited to laxity of base thread
                    i_sum += max(0.0, min(i_sum_tmp, base_thr.deadline - base_thr.exec_time + 1.0))
                i_sum = math.floor(i_sum / self.num_core)
                i_sum_list.append(i_sum)

            print('i_sum_list')
            print(i_sum_list)

            """
            Find minimum possible option for each tasks.
            Compare with interference vs parallel option table created earlier.
            The option is always non decreasing.
            Increment option until it can tolerate calculated interference.
            """
            selected_opt_cpy = selected_opt[:]
            for i in range(n_task):
                while selected_opt[i] < self.max_opt:
                    # floating value comparison... difference less than 0.1
                    if i_sum_list[i] > self.ip_table[i][selected_opt[i]] + 0.1:
                        selected_opt[i] += 1
                    else:
                        break
            print('selected_opt')
            print(selected_opt)

            # if no change needed, check convergence
            if selected_opt == selected_opt_cpy:
                """
                if any parallel option maxed out, but still its interference
                exceeds tolerance --> unschedulable
                else --> schedulable
                """
                for i in range(n_task):
                    # popt maxed out
                    if selected_opt[i] >= self.max_opt:
                        # interference exceeds tolerance
                        if i_sum_list[i] > self.ip_table[i][selected_opt[i]] + 0.1:
                            print('*unschedulable, with option')
                            print(selected_opt)
                            return False, selected_opt
                # All tasks interference under tolerance
                print('schedulable, with option')
                print(selected_opt)
                return True

            # print('----------------')

    def is_schedulable_dbg(self, pts, popt_list):
        # Test schedulability of a task set with given option using CHO.
        self.create_inter_vs_popt_table(pts)

        print('ip_table_dbg')
        print(self.ip_table)

        pts.popt_strategy = 'custom'
        pts.popt_list = popt_list
        pts.serialize_pts()

        n_task = len(pts.pt_list)

        # Calculate interference of other threads.
        i_sum_list = []
        for i in range(n_task):
            # check only the first thread of each task.
            base_thr = pts.pt_list[i][popt_list[i]][0]
            i_sum = 0.0
            for j in range(len(pts)):
                inter_thr = pts[j]
                if inter_thr == base_thr:
                    continue
                i_sum_tmp = tsutil.workload_in_interval_edf(inter_thr, base_thr.deadline)
                # interference is limited to laxity of base thread
                i_sum += max(0.0, min(i_sum_tmp, base_thr.deadline - base_thr.exec_time + 1.0))
            i_sum = math.floor(i_sum / self.num_core)
            # print('i_sum')
            # print(i_sum)
            i_sum_list.append(i_sum)

        print('i_sum_list_dbg')
        print(i_sum_list)
        # Test schedulability
        for i in range(n_task):
            if i_sum_list[i] > self.ip_table[i][popt_list[i]] + 0.1:
                return False
        return True

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
