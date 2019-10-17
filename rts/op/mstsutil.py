import math


def workload_in_interval_edf(t, l):
    # body job
    # tasks aligned to deadlines
    num_body_job = math.floor(l / t.period)
    w_body_job = t.exec_time * num_body_job

    # carry-in
    # slack not defined
    if not hasattr(t, 'slack'):
        t.slack = 0.0
    w_carry_in = math.fmod(l, t.period) - t.slack
    # carry-in has to be positive
    if w_carry_in < 0.0:
        w_carry_in = 0.0
    # carry-in cannot exceed the actual execution time
    w_carry_in = min(t.exec_time, w_carry_in)

    return w_body_job + w_carry_in
