import math


def dbf(t, interval):
    # DBF(tau, t) = max(0, (|_(t - Di) / Ti _| + 1 ) * Ci)
    num_task = math.floor((interval - t.deadline) / t.period)
    return max(0.0, t.exec_time * (num_task + 1.0))


def dbf_prime(t, interval):
    # DBF'(tau, t) = |_ t / Ti _| * CI + min(Ci, t mod Ti)
    whole_inclusion = math.floor(interval / t.period)
    carry_in = min(t.exec_time, math.fmod(interval, t.period))
    return whole_inclusion + carry_in


def calc_extended_interval_bound(ts):

    pass


def calc_i1():
    pass


def calc_i2():
    pass


def calc_interference():
    pass


def is_schedulable(ts, **kwargs):
    num_core = float(kwargs.get('num_core', 1.0))
    pass