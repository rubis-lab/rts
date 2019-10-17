from rts.popt.popt import Popt
from rts.op import tsutil
from rts.op import mstsutil
import math


class ChoMultiSegmentTask(Popt):
    'Cho Multi Segment Task'

    def __init__(self, **kwargs):
        self.max_opt = kwargs.get('max_option', 1)
        self.num_core = float(kwargs.get('num_core', 1.0))
        self.ip_table = []
        self.tolerance_table = []
        self.inc_strategy = kwargs.get('inc_strategy', 'naive')
        return

    def __del__(self):
        return

    def __str__(self):
        info = ''
        return info

    def create_tolerance_table(self, msts):
        del self.tolerance_table[:]

        for i, mst in enumerate(msts):
            self.tolerance_table.append([-1.0])  # option 0 will not be used

            mst.popt_strategy = 'single'  # start from single
            mst.update_ts_list()
            self.tolerance_table[i].append(mst.deadline - mst.crit_exec_time)

            mst.max_opt_ms = 1
            if self.inc_strategy == 'naive':
                mst.max_opt_ms = mst.max_opt
            elif self.inc_strategy == 'fdsf':
                n_seg = len(mst)
                mst.max_opt_ms = (mst.max_opt - 1) ** n_seg
            elif self.inc_strategy == 'cdsf':
                n_seg = len(mst)
                mst.max_opt_ms = (mst.max_opt - 1) ** n_seg
            else:
                print('Increment strategy not defined.')

            for _ in range(1, mst.max_opt_ms):
                if self.inc_strategy == 'naive':
                    mst.increment_naive()
                elif self.inc_strategy == 'fdsf':
                    mst.increment_fdsf()
                elif self.inc_strategy == 'cdsf':
                    mst.increment_cdsf()
                else:
                    print('Increment strategy not defined.')

                self.tolerance_table[i].append(mst.deadline - mst.crit_exec_time)
        return

    def is_schedulable(self, msts):
        # Create interference vs parallel option table for every task
        self.create_tolerance_table(msts)
        # print('tolerance_table')
        # print(self.tolerance_table)

        # Initial - all tasks at lowest parallelization
        for mst in msts:
            mst.popt_strategy = 'single'
            mst.update_ts_list()

        n_task = len(msts)
        selected_opt = [1 for _ in range(n_task)]

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

            for base_mst in msts:
                i_sum = 0.0
                for inter_mst in msts:
                    if inter_mst == base_mst:
                        continue
                    i_sum_tmp = mstsutil.bounded_workload_in_interval_edf(
                        inter_mst,
                        base_mst.deadline,
                        base_mst.deadline - base_mst.crit_exec_time + 1.0)

                    i_sum += max(0.0, i_sum_tmp)
                i_sum = math.floor(i_sum / self.num_core)
                i_sum_list.append(i_sum)

            # for i in range(n_task):
            #     msts[i].popt_strategy = 'custom'
            #     n_seg = len(msts[i])
            #     popt_list = [selected_opt[i] for _ in range(n_seg)]  # naive raising
            #     msts[i].popt_list = popt_list
            #     msts[i].update_ts_list()
            #     base_task = msts[i]
            #
            #     i_sum = 0.0
            #     for j in range(n_task):
            #         inter_task = msts[j]
            #         if inter_task == base_task:
            #             continue
            #         i_sum_tmp = tsutil.workload_in_interval_edf(inter_task, base_task.deadline)
            #         # interference is limited to laxity of base thread
            #         i_sum += max(0.0, min(i_sum_tmp, base_task.deadline - base_task.crit_exec_time + 1.0))
            #     i_sum = math.floor(i_sum / self.num_core)
            #     # print('i_sum')
            #     # print(i_sum)
            #     i_sum_list.append(i_sum)

            """
            Find minimum possible option for each tasks.
            Compare with interference vs parallel option table created earlier.
            The option is always non decreasing.
            Increment option until it can tolerate calculated interference.
            """
            selected_opt_cpy = selected_opt[:]
            for i, mst in enumerate(msts):
                while selected_opt[i] < mst.max_opt_ms:
                    # floating value comparison... difference less than 0.1
                    if i_sum_list[i] > self.tolerance_table[i][selected_opt[i]] + 0.1:
                        selected_opt[i] += 1
                        if self.inc_strategy == 'naive':
                            mst.increment_naive()
                        elif self.inc_strategy == 'fdsf':
                            mst.increment_fdsf()
                        elif self.inc_strategy == 'cdsf':
                            mst.increment_cdsf()
                        else:
                            print('Increment strategy not defined.')
                    else:
                        break

            # for i in range(n_task):
            #     while selected_opt[i] < self.max_opt:
            #         # floating value comparison... difference less than 0.1
            #         if i_sum_list[i] > self.tolerance_table[i][selected_opt[i]] + 0.1:
            #             selected_opt[i] += 1
            #         else:
            #             break
            # print('selected_opt')
            # print(selected_opt)

            # if no change needed, check convergence
            if selected_opt == selected_opt_cpy:
                """
                if any parallel option maxed out, but still its interference
                exceeds tolerance --> unschedulable
                else --> schedulable
                """
                for i, mst in enumerate(msts):
                    # popt maxed out
                    if selected_opt[i] >= mst.max_opt_ms:
                        # interference exceeds tolerance
                        if i_sum_list[i] > self.tolerance_table[i][selected_opt[i]] + 0.1:
                            return False, selected_opt  # false

                # for i in range(n_task):
                #     # popt maxed out
                #     if selected_opt[i] >= self.max_opt:
                #         # interference exceeds tolerance
                #         if i_sum_list[i] > self.tolerance_table[i][selected_opt[i]] + 0.1:
                #             return False, selected_opt  # false
                # All tasks interference under tolerance
                # print(selected_opt)
                # print('selected_opt')
                # Update all options

                # for i in range(n_task):
                #     msts[i].popt_strategy = 'custom'
                #     n_seg = len(msts[i])
                #     msts[i].popt_list = [selected_opt[i] for _ in range(n_seg)]  # naive raising
                #     msts[i].update_ts_list()

                # print('serialized----------')
                # print(pts.pts_serialized)
                return True, selected_opt  # true
