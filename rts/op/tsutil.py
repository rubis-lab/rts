import math


def calc_utilization(t):
    return t.exec_time / t.period


def sum_utilization(ts):
    sum = 0.0
    for t in ts:
        sum += calc_utilization(t)
    return sum


def calc_density(t):
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


def workload_in_interval_edf(t, l):
    # body job
    # tasks aligned to deadlines
    num_body_job = math.floor(l / t.period)
    w_body_job = t.exec_time * num_body_job

    # carry-in
    # ??? check if slack not defined
    w_carry_in = math.fmod(t.deadline, t.period) - t.slack
    # carry-in has to be positive
    if w_carry_in < 0.0:
        w_carry_in = 0.0
    # carry-in cannot exceed the actual execution time
    w_carry_in = min(t.exec_time, w_carry_in)

    return w_body_job + w_carry_in


def workload_in_interval_fp(t, l):
    # body job
    num_body_job = math.floor((l + t.deadline - t.exec_time - t.slack) / t.period)
    w_body_job = t.exec_time * num_body_job

    # carry-out
    w_carry_out = l + t.deadline - t.exec_time - t.period * num_body_job

    # carry-out cannot exceed the actual execution time
    w_carry_out = math.min(t.exec_time, w_carry_out)
    
    return w_body_job + w_carry_out
