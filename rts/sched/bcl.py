import math

# Each task's slack is tracked
slack = []


def calc_interference(base_task, inter_task):
    n_inter_task = math.floor(base_task.deadline / inter_task.period)

    carry_in = math.fmod(base_task.deadline, inter_task.period) \
        - slack[inter_task.id]

    if carry_in < 0.0:
        carry_in = 0.0

    jk = inter_task.exec_time * n_inter_task \
        + min(inter_task.exec_time, carry_in)

    interference = min(jk, base_task.deadline - base_task.exec_time + 1.0)

    return interference


def is_schedulable(ts, **kwargs):
    num_core = float(kwargs.get('num_core', 1.0))

    del slack[:]
    for i in range(len(ts)):
        slack.append(0.0)

    # Terminate condition
    updated = True
    while updated:
        updated = False

        # Check each task's feasibility
        sched = True
        for base_task in ts:

            # Add up all demands from interfering tasks
            sum_j = 0.0
            for inter_task in ts:
                if base_task.id != inter_task.id:
                    sum_j += calc_interference(base_task, inter_task)
            sum_j = math.floor(sum_j / num_core)

            slack_tmp = base_task.deadline - base_task.exec_time - sum_j

            # slack < 0 --> infeasible
            if slack_tmp < 0.0:
                sched = False

            # continue if slack is updated
            elif slack_tmp > slack[base_task.id]:
                slack[base_task.id] = slack_tmp
                updated = True

        if sched:
            return True

    return False
