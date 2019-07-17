import math
from rts.sched.sched import Sched
from rts.op import tsutil


class BAR(Sched):
    def __init__(self, **kwargs):
        self.num_core = float(kwargs.get('num_core', 1.0))

    def calc_ext_interval(self, ts):
        k = min(len(ts), int(self.num_core - 1))
        k_max_tasks = tsutil.get_k_max_exec_time_task(ts, k)
        # print(ts)
        # C_sum
        c_sum = 0.0
        for t in k_max_tasks:
            c_sum += t.exec_time

        a_k_base = c_sum
        for t in ts:
            a_k_base += (t.period - t.deadline) * tsutil.calc_utilization(t)

        # print('a_k_base: ' + str(a_k_base))

        # Ak = [AkBase + Dk * Utot - m * Dk + m * Ck ] / [m - Utot]
        a_k_list = []
        for t in ts:
            a_k_rem = t.deadline * (tsutil.sum_utilization(ts) - self.num_core) + self.num_core * t.exec_time
            a_k_rem = (a_k_base + a_k_rem) / (self.num_core - tsutil.sum_utilization(ts))
            a_k_list.append(a_k_rem)

        return a_k_list

    def calc_non_ci_interference(self, base_task, inter_task, ext_interval):
        dbf = tsutil.workload_in_interval_edf_whole(inter_task, ext_interval + base_task.deadline)

        if base_task is inter_task:
            # min(DBF(ti, ak + dk) - ck, ak)	(i == k)
            return min(dbf - inter_task.exec_time, ext_interval)
        else:
            # min(DBF(ti, ak + dk), ak + dk - ck)
            return min(dbf, ext_interval + base_task.deadline - base_task.exec_time)

    def calc_ci_interference(self, base_task, inter_task, ext_interval):
        dbf_prime = tsutil.workload_in_interval_edf(inter_task, ext_interval + base_task.deadline)

        if base_task is inter_task:
            # min(DBF'(ti, Ak + Dk) - Ck, Ak)
            return min(dbf_prime - base_task.exec_time, ext_interval)
        else:
            # min(DBF'(ti, Ak + Dk), Ak + Dk - Ck)
            return min(dbf_prime, ext_interval + base_task.deadline - base_task.exec_time)

    def is_schedulable(self, ts):
        # trivial condition
        if tsutil.sum_utilization(ts) <= 1.0:
            return True
        if tsutil.sum_utilization(ts) > self.num_core:
            return False
        # Dk > Ck
        for t in ts:
            if tsutil.calc_density(t) > 1.0:
                return False

        a_k_list = self.calc_ext_interval(ts)
        # print(a_k_list)

        for base_task_idx, base_task in enumerate(ts):
            # Ak <= 0, don't need to check
            if a_k_list[base_task_idx] < 0:
                # print(str(base_task_idx) + ': ' + str(a_k_list[base_task_idx]) + ' is below 0')
                continue
            # print('base_task_idx: ' + str(base_task_idx))

            ext_interval = 0.0
            # iterate with Ak
            while ext_interval < a_k_list[base_task_idx]:
                # non ci
                interference_list_non_ci = []
                for inter_task in ts:
                    interference_list_non_ci.append(
                        self.calc_non_ci_interference(base_task, inter_task, ext_interval))

                # ci
                interference_list_ci = []
                for inter_task in ts:
                    interference_list_ci.append(
                        self.calc_ci_interference(base_task, inter_task, ext_interval))

                # non ci vs ci diff
                interference_diff_list = []
                for idx in range(len(ts)):
                    diff = interference_list_ci[idx] - interference_list_non_ci[idx]
                    if diff < 0:
                        print('interference_diff calc error')
                    interference_diff_list.append(diff)

                # m - 1 largest carry-in
                interference_diff_list.sort(reverse=True)
                k = min(len(ts), int(self.num_core) - 1)
                k_largest_ci = interference_diff_list[:k]

                # sum up interferences.
                tot_interference = 0.0
                for interference in interference_list_non_ci:
                    tot_interference += interference
                for additional_interference in k_largest_ci:
                    tot_interference += additional_interference

                # not schedulable RHS: m(Ak + Dk - Ck)
                if tot_interference > self.num_core * (base_task.deadline - base_task.exec_time + ext_interval):
                    return False

                ext_interval += 1.0

        return True
