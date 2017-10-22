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
