import math


def calc_whole_inclusion(base_task, inter_task, offset):
    if offset >= base_task.deadline:
        return 0.0

    n_inter_task = math.floor((base_task.deadline -
                               offset) / inter_task.period)

    return n_inter_task * inter_task.exec_time


def calc_carry_in_using_slack(base_task, inter_task, offset):
    if offset >= base_task.deadline:
        return 0.0

    # carry-ins calculated from slack values
    carry_in = math.fmod(base_task.deadline - offset,
                         inter_task.period) - inter_task.slack

    # carry-in has to be positive
    if carry_in < 0.0:
        carry_in = 0.0

    # carry-in cannot exceed the actual execution time
    return min(inter_task.exec_time, carry_in)


def calc_offsets(ts, base_task, inter_task):
    # calculates relative offsets from interfering task's deadline
    base_interval = base_task.deadline
    rem1 = math.fmod(base_interval, inter_task.period)

    offsets = []
    for t in ts:
        rem2 = math.fmod(base_interval, t.period)
        if rem1 >= rem2:
            offsets.append(rem1 - rem2)
        else:
            offsets.append(rem1 - rem2 + t.period)

    return offsets


def calc_interference_using_slack(base_task, inter_task, offset):
    # calculate carry-ins with slack values
    # not considering actual release pattern
    i_sum = 0.0

    # tasks are not aligned to their deadlines
    i_sum += calc_whole_inclusion(base_task, inter_task, offset)

    # carry-ins calculated from slack values
    i_sum += calc_carry_in_using_slack(base_task, inter_task, offset)

    # interference is limited to leftover of basetask
    # i_sum = min(i_sum, base_task.deadline - base_task.exec_time + 1.0)
    i_sum = min(i_sum, base_task.deadline - base_task.exec_time)

    return i_sum


def calc_carry_in(ts, rem_interval, base_task, offsets, num_core):
    # calculates carry-in based on relative position of tasks

    # sum up other task's interference
    sum_j = 0.0
    inter_task_idx = 0
    for inter_task in ts:
        if inter_task != base_task:
            # use naive interference, calculation with slack
            # this is to limit the calculation depth
            sum_j += calc_interference_using_slack(
                base_task, inter_task, offsets[inter_task_idx])

        inter_task_idx += 1

    # sum_j = math.floor(sum_j / num_core)
    sum_j = sum_j / num_core

    slack = base_task.deadline - base_task.exec_time - sum_j

    if slack < 0.0:
        slack = 0.0

    carry_in = rem_interval - slack
    if carry_in < 0.0:
        carry_in = 0.0

    # carry-in limited to execution time
    carry_in = min(carry_in, base_task.exec_time)

    return carry_in


def calc_rem_interval(base_task, inter_task):
    rem_interval = math.fmod(base_task.deadline, inter_task.period)
    return rem_interval


def calc_interference(ts, base_task, inter_task, num_core):
    i_sum = 0.0

    # here, all tasks are aligned at their deadlines
    i_sum += calc_whole_inclusion(base_task, inter_task, 0.0)

    # to calculate carry-in, current relative execution is needed
    offsets = calc_offsets(ts, base_task, inter_task)

    # calculation of carry-in is done according to the relative execution
    # note in this case, the base interval is actually
    # the interfering task's interval
    # also note that rem_interval is the leftover of interfering task
    # this interval will be used to limit the carry-in
    rem_interval = calc_rem_interval(base_task, inter_task)

    i_sum += calc_carry_in(ts, rem_interval, inter_task, offsets, num_core)

    # interference is limited to leftover of basetask
    # i_sum = min(i_sum, base_task.deadline - base_task.exec_time + 1.0)
    i_sum = min(i_sum, base_task.deadline - base_task.exec_time)

    return i_sum


def calc_slack(ts, base_task, num_core):
    # Add up all demands from interfering tasks
    sum_j = 0.0
    for inter_task in ts:
        if base_task != inter_task:
            sum_j += calc_interference(ts, base_task, inter_task, num_core)

    # sum_j = math.floor(sum_j / num_core)
    sum_j = sum_j / num_core

    # slack is leftover cpu time after job completion
    slack_tmp = base_task.deadline - base_task.exec_time - sum_j
    return slack_tmp


def is_schedulable(ts, **kwargs):
    num_core = float(kwargs.get('num_core', 1.0))

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
            slack_tmp = calc_slack(ts, base_task, num_core)

            # slack < 0 --> infeasible
            if slack_tmp < 0.0:
                sched = False

            # continue if slack is updated
            elif slack_tmp > base_task.slack:
                base_task.slack = slack_tmp
                updated = True

        if sched:
            return True

    return False
