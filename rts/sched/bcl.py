import math
from rts.sched.sched import Sched
from rts.op import tsutil

class BCL(Sched):
    def __init__(self, **kwargs):
        self.num_core = float(kwargs.get('num_core', 1.0))

    # def calc_whole_inclusion(self, base_task, inter_task):
    #     n_inter_task = math.floor(base_task.deadline / inter_task.period)

    #     return n_inter_task * inter_task.exec_time

    # def calc_carry_in_using_slack(self, base_task, inter_task):
    #     # carry-ins calculated from slack values
    #     carry_in = math.fmod(base_task.deadline, inter_task.period) \
    #         - inter_task.slack

    #     # carry-in has to be positive
    #     if carry_in < 0.0:
    #         carry_in = 0.0

    #     # carry-in cannot exceed the actual execution time
    #     return min(inter_task.exec_time, carry_in)

    def calc_interference(self, base_task, inter_task):
        # i_sum = 0.0

        # # threads aligned to deadlines
        # i_sum += self.calc_whole_inclusion(base_task, inter_task)

        # # carry-ins
        # i_sum += self.calc_carry_in_using_slack(base_task, inter_task)

        i_sum = tsutil.workload_in_interval_edf(inter_task, base_task.deadline)

        # interference is limited to leftover of basetask
        i_sum = max(0.0, min(i_sum, base_task.deadline - base_task.exec_time))

        return i_sum

    def calc_slack(self, ts, base_task):
        # Add up all demands from interfering tasks
        sum_j = 0.0
        for inter_task in ts:
            if base_task != inter_task:
                sum_j += self.calc_interference(base_task, inter_task)

        # sum_j = math.floor(sum_j / self.num_core)
        sum_j = sum_j / self.num_core

        # slack is leftover cpu time after job completion
        return base_task.deadline - base_task.exec_time - sum_j

    def is_schedulable(self, ts):
        tsutil.reset_slack(ts)
        # init slack of each task
        for t in ts:
            t.slack = 0.0

        # Terminate condition
        updated = True
        while updated:
            updated = False

            # Check each task's feasibility
            sched = True
            for base_task in ts:

                # Update slack
                slack_tmp = self.calc_slack(ts, base_task)

                # slack < 0 --> infeasible
                if slack_tmp < -0.01:
                    sched = False

                # continue if slack is updated
                elif slack_tmp > base_task.slack + 0.01:
                    base_task.slack = slack_tmp
                    updated = True

            if sched:
                tsutil.reset_slack(ts)
                return True

        tsutil.reset_slack(ts)
        return False
