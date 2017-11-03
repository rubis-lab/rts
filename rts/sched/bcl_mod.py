import math


def calc_interference(base_thr, inter_thr):
    n_inter_thr = math.floor(base_thr.deadline / inter_thr.period)

    carry_in = math.fmod(base_thr.deadline, inter_thr.period)\
        - inter_thr.slack

    if carry_in < 0.0:
        carry_in = 0.0

    jk = inter_thr.exec_time * n_inter_thr \
        + min(inter_thr.exec_time, carry_in)

    interference = min(jk, base_thr.deadline - base_thr.exec_time + 1.0)

    return interference


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

            # Add up all demands from interfering tasks
            sum_j = 0.0
            for inter_thr in pts:
                if base_thr != inter_thr:
                    sum_j += calc_interference(base_thr, inter_thr)
            sum_j = math.floor(sum_j / num_core)

            slack_tmp = base_thr.deadline - base_thr.exec_time - sum_j

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
