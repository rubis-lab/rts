import math


def calc_utilization(t):
    if hasattr(t, 'total_exec_time'):
        return t.total_exec_time / t.period
    return t.exec_time / t.period


def sum_utilization(ts):
    sum = 0.0
    for t in ts:
        sum += calc_utilization(t)
    return sum


def calc_density(t):
    if hasattr(t, 'total_exec_time'):
        return t.total_exec_time / t.deadline
    return t.exec_time / t.deadline


def sum_density(ts):
    sum = 0.0
    for t in ts:
        sum += calc_density(t)
    return sum


def max_utilization(ts):
    list = []
    for t in ts:
        list.append(calc_utilization(t))
    return max(list)


def max_density(ts):
    list = []
    for t in ts:
        dens = calc_density(t)
        list.append(dens)
        # list.append(calc_density(t))
    return max(list)


def workload_in_interval_edf(t, _l):
    # body job
    # tasks aligned to deadlines
    num_body_job = math.floor(_l / t.period)
    w_body_job = t.exec_time * num_body_job

    # carry-in
    w_carry_in = math.fmod(_l, t.period) - t.slack
    # print('s {} {}'.format(w_carry_in, t.slack))
    # carry-in has to be positive
    if w_carry_in < 0.0:
        w_carry_in = 0.0
    # carry-in cannot exceed the actual execution time
    w_carry_in = min(t.exec_time, w_carry_in)

    return w_body_job + w_carry_in


def workload_in_interval_edf_whole(t, _l):
    # body job
    # tasks aligned to deadlines
    num_body_job = math.floor(_l / t.period)
    w_body_job = t.exec_time * num_body_job

    return w_body_job


def workload_in_interval_dbf(t, _l):
    num_body_job = math.floor((_l - t.deadline) / t.period)

    w_body_job = t.exec_time * (num_body_job + 1.0)

    return w_body_job


def get_k_max_exec_time_task(ts, k=1):
    tasks = ts.task_list
    tasks.sort(key=lambda x: x.exec_time)

    return tasks[:k]


def workload_in_interval_fp(t, _l):
    # body job
    if t.slack > 0.1:
        print('sss!')
    num_body_job = \
        math.floor((_l + t.deadline - t.exec_time - t.slack) / t.period)
    w_body_job = t.exec_time * num_body_job
    print('w_body_job')
    print(w_body_job)

    # carry-out
    w_carry_out = \
        _l + t.deadline - t.exec_time - t.period * num_body_job - t.slack
    print('w_carry_out_orig')
    print(w_carry_out)

    # carry-out cannot exceed the actual execution time
    w_carry_out = min(t.exec_time, w_carry_out)

    # carry-out cannot exceed the length of the interval
    w_carry_out = min(_l, w_carry_out)

    print('w_carry_out')
    print(w_carry_out)

    return w_body_job + w_carry_out


def reset_slack(ts):
    for t in ts:
        t.slack = 0.0
    return
