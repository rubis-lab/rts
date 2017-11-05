import math


def calc_whole_inclusion(base_thr, inter_thr, offset):
    n_inter_thr = math.floor(base_thr.deadline - offset / inter_thr.period)

    return n_inter_thr * inter_thr.exec_time


def calc_offsets(pts, base_thr, inter_thr):
    base_interval = base_thr.deadline
    rem1 = math.fmod(base_interval, inter_thr.period)

    offsets = []
    for thr in pts:
        rem2 = math.fmod(base_interval, thr.period)
        if rem1 >= rem2:
            offsets.append(rem1 - rem2)
        else:
            offsets.append(rem1 - rem2 + thr.period)

    return offsets


def calc_interference_using_slack(base_thr, inter_thr, offset):
    # calculate carry-ins with slack values
    # not considering actual release pattern
    i_sum = 0.0

    # threads are not aligned to their deadlines
    i_sum += calc_whole_inclusion(base_thr, inter_thr, offset)

    # carry-ins calculated from slack values
    carry_in = math.fmod(base_thr.deadline - offset, inter_thr.period)\
        - inter_thr.slack

    # carry-in has to be positive
    # carry-in cannot exceed the actual execution time
    if carry_in < 0.0:
        carry_in = 0.0
    i_sum += min(inter_thr.exec_time, carry_in)

    return i_sum


def calc_carry_in(pts, rem_interval, base_thr, offsets, num_core):
    # calculates carry-in based on relative position of threads

    # sum up other thread's interference
    sum_j = 0.0
    inter_thr_idx = 0
    for inter_thr in pts:
        if inter_thr != base_thr:
            # use naive interference, calculation with slack
            # this is to limit the calculation depth
            sum_j += calc_interference_using_slack(
                base_thr, inter_thr, offsets[inter_thr_idx])

        inter_thr_idx += 1

    sum_j = math.floor(sum_j / num_core)

    slack = base_thr.deadline - base_thr.exec_time - sum_j

    if slack < 0.0:
        slack = 0.0

    carry_in = rem_interval - slack
    if carry_in < 0.0:
        carry_in = 0.0

    return carry_in


def calc_interference(pts, base_thr, inter_thr, num_core):
    i_sum = 0.0

    # here, all threads are aligned at their deadlines
    i_sum += calc_whole_inclusion(base_thr, inter_thr, 0.0)

    # to calculate carry-in, current relative execution is needed
    offsets = calc_offsets(pts, base_thr, inter_thr)

    # calculation is done according to the relative execution
    # note in this case, base interval is actually
    # the interfering task's interval
    # also note rem_interval is the leftofver of interfereing thread
    rem_interval = math.fmod(base_thr.deadline, inter_thr.period)

    i_sum += calc_carry_in(pts, rem_interval, inter_thr, offsets, num_core)

    return i_sum


def calc_slack(pts, base_thr, num_core):
    # Add up all demands from interfering tasks
    sum_j = 0.0
    for inter_thr in pts:
        if base_thr != inter_thr:
            sum_j += calc_interference(pts, base_thr, inter_thr, num_core)

    sum_j = math.floor(sum_j / num_core)

    # slack is leftover cpu time after job completion
    slack_tmp = base_thr.deadline - base_thr.exec_time - sum_j
    return slack_tmp


def is_schedulable(pts, **kwargs):
    num_core = float(kwargs.get('num_core', 1.0))

    # init slack of each task
    for thr in pts:
        thr.slack = 0.0

    # Terminate condition
    updated = True
    while updated:
        updated = False

        # Check each task's feasibility
        sched = True
        for base_thr in pts:

            # Update slack
            slack_tmp = calc_slack(pts, base_thr, num_core)

            # slack < 0 --> infeasible
            if slack_tmp < 0.0:
                sched = False

            # continue if slack is updated
            elif slack_tmp > base_thr.slack:
                base_thr.slack = slack_tmp
                updated = True

        if sched:
            return True

    return True
