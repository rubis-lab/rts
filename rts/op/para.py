from rts.core.ts import TaskSet
from rts.core.thr import Thread
import random
import operator
import math


def parallelize_alpha(pt):
    # Parallelize task while non decreasing total execution time
    # Also largest execution time always non increases

    # total execution time
    # required to have total execution time larger than 3 * max_option
    e_tot = pt.base_task.exec_time
    if e_tot <= pt.max_opt * 3:
        raise Exception('Execution time too small')
    e_tot_prev = e_tot

    # largest execution time
    e_max = pt.base_task.exec_time
    e_max_prev = e_max

    for opt in range(2, pt.max_opt + 1):
        pt.ts_table[str(opt)] = TaskSet()

        # increase total execution time
        e_tot = e_tot_prev * (1.0 + pt.variance)

        # decrease first thread execution time accordingly
        e_max = e_max_prev - ((e_tot - e_tot_prev) / pt.overhead)

        # ideal seperation execution time
        e_ideal = e_tot / opt

        """
        normalize variance
        variance = 0 --> e_max = e_ideal
        variance = 1 --> e_max = e_max (prev)

        e_max_limit = e_ideal + (e_max(prev) - e_ideal) * variance

        unifast split into pcs,
        while only accepting when largest generated e < e_max_limit
        """

        # execution times
        e_max_limit = e_ideal + (e_max - e_ideal) * pt.variance
        e_list = unifast_divide(opt, e_tot, e_max_limit)
        e_max = e_list[0]

        # create threads and append to task set
        ts = TaskSet()

        for i in range(len(e_list)):

            # set minimum e to 1.0
            if e_list[i] < 0.1:
                e_list[i] = 1.0

            thr_param = {
                'id': pt.base_task.id,
                'exec_time': e_list[i],
                'deadline': pt.base_task.deadline,
                'period': pt.base_task.period,
            }
            thr = Thread(**thr_param)

            ts.append(thr)

        # append to pt
        pt.ts_table[str(opt)] = ts

        e_tot_prev = e_tot
        e_max_prev = e_max

    return


def parallelize_task(t, **kwargs):
    pcs = kwargs.get('pcs', 1)
    overhead = float(kwargs.get('overhead', random.random()))
    variance = float(kwargs.get('variance', random.random()))

    """
    overhead = 0 --> Ck
             = 1 --> Opt * Ck
    Ck * [1 + (m - 1) * overhead]
    """
    #
    new_exec_time = t.exec_time \
        * (1.0 + (pcs - 1.0) * overhead)
    new_exec_time = new_exec_time / pcs

    """
    normalize variance
    variance = 0 --> max 0 difference
    a = Ck' .. b = Ck'
    variance = 1 --> max Ck difference
    a = 0   .. b = Ck

    a = Ck'(1 - variance)
    b = Ck'(1 + (Ck - Ck') * variance)
    """
    a = new_exec_time * \
        (1.0 - variance)
    b = new_exec_time * \
        (1.0 + (t.exec_time - new_exec_time) * variance)

    thr_list = []
    for i in range(pcs):
        thr_param = {
            'id': t.id,
            'exec_time': round(random.uniform(a, b), 0),
            'deadline': t.deadline,
            'period': t.period,
        }
        thr = Thread(**thr_param)

        thr_list.append(thr)

    # Sorts threads in execution time descending order.
    thr_list.sort(key=operator.attrgetter('exec_time'))

    # Set thread ID
    idx = 0
    for thr in thr_list:
        thr.tid = idx
        idx += 1

    return thr_list


def unifast_divide(pcs, tot, limit):
    max_iter = 25
    divided_best_effort = [10000000]
    for ll in range(max_iter):
        divided = []
        tot_sum = tot
        for i in range(pcs - 1):
            tmp = tot_sum * math.pow(
                random.uniform(0.0, 1.0), (1.0 / (pcs - i)))
            # round to integer
            tmp = round(tmp)
            divided.append(tot_sum - tmp)
            tot_sum = tmp
        divided.append(tot_sum)

        # Return only when largest value is under limit
        if max(divided) <= limit:
            divided.sort(reverse=True)
            return divided

        # Save the pseudo sufficient value
        if max(divided) < max(divided_best_effort):
            divided_best_effort = divided[:]

    divided_best_effort.sort(reverse=True)
    return divided_best_effort


def parallelize_pt_non_dec(pt):
    # Paralleliuze task while non decreasing total execution time
    # Also largest execution time always non increases

    # total execution time
    # required to have total execution time larger than 3 * max_option
    e_tot = pt.base_task.exec_time
    if e_tot <= pt.max_opt * 3:
        raise Exception('Execution time too small')

    # largest execution time
    e_max = pt.base_task.exec_time

    # # debug
    # e_tot_prev = e_tot
    # e_max_prev = e_max

    for opt in range(2, pt.max_opt + 1):
        pt.ts_table[str(opt)] = TaskSet()

        # total execution time is increased by overhead
        e_tot = math.ceil(e_tot * (1.0 + pt.overhead))

        # ideal seperation execution time
        e_ideal = e_tot / opt

        """
        normalize variance
        variance = 0 --> e_max = e_ideal
        variance = 1 --> e_max = e_max (prev)

        e_max_limit = e_ideal + (e_max(prev) - e_ideal) * variance

        unifast split into pcs,
        while only accepting when largest generated e < e_max_limit
        """

        # execution times
        e_max_limit = e_ideal + (e_max - e_ideal) * pt.variance
        e_list = unifast_divide(opt, e_tot, e_max_limit)
        e_max = e_list[0]

        # create threads and append to task set
        ts = TaskSet()

        for i in range(len(e_list)):

            # set minimum e to 1.0
            if e_list[i] < 0.1:
                e_list[i] = 1.0

            thr_param = {
                'id': pt.base_task.id,
                'exec_time': e_list[i],
                'deadline': pt.base_task.deadline,
                'period': pt.base_task.period,
            }
            thr = Thread(**thr_param)

            ts.append(thr)
        # # debug
        # if e_max_prev > e_max:
        #   real_alpha = (e_tot - e_tot_prev) / (e_max_prev - e_max)
        #   print('real_alpha: ' + str(real_alpha))
        # e_max_prev = e_max
        # e_tot_prev = e_tot

        # append to pt
        pt.ts_table[str(opt)] = ts
    return


def unifast_divide_alpha(pcs, tot, limit):
    max_iter = 25
    divided_best_effort = [10000000]
    for ll in range(max_iter):
        divided = []
        tot_sum = tot
        for i in range(pcs - 1):
            tmp = tot_sum * math.pow(
                random.uniform(0.0, 1.0), (1.0 / (pcs - i)))
            # round to integer
            tmp = round(tmp)
            divided.append(tot_sum - tmp)
            tot_sum = tmp
        divided.append(tot_sum)

        # Return only when largest value is under limit
        if max(divided) <= limit:
            divided.sort(reverse=True)
            return divided

        # Save the pseudo sufficient value
        if max(divided) < max(divided_best_effort):
            divided_best_effort = divided[:]

    divided_best_effort.sort(reverse=True)
    return divided_best_effort


def normalize_list(_l):
    l_sum = sum(_l)
    l_mean = l_sum / len(_l)

    return [(ll - l_mean) / l_sum for ll in _l]


def parallelize_pt_non_dec_alpha(pt):
    # Parallelize task while non decreasing total execution time
    # largest execution time always non increases

    # total execution time
    # required to have total execution time larger than 3 * max_option
    e_tot = pt.base_task.exec_time
    if e_tot <= pt.max_opt * 3:
        raise Exception('Execution time too small')

    # largest execution time
    e_max = pt.base_task.exec_time

    e_tot_prev = e_tot
    e_max_prev = e_max

    for opt in range(2, pt.max_opt + 1):
        # print('----------------')
        # print('opt: ' + str(opt))
        e_mean = e_tot_prev / opt
        # print('e_mean: ' + str(e_mean))

        # random draw (opt) from [0, 1]
        # fixed s_tot, which is scaled later
        # necessary step, to keep the ratio same
        # discard if max thread is larger than before.
        max_effort = 10
        effort = 0
        while True:
            if effort >= max_effort:
                break

            s_tot = 1000
            s_list = unifast_divide(opt, s_tot, (s_tot / opt) *
                (1.0 + pt.variance))
            s_list_norm = normalize_list(s_list)
            # print(s_list_norm)

            e_list = [round(e_mean * (1.0 + s)) for s in s_list_norm]
            # print('e_list: ' + str(e_list))

            e_max = max(e_list)
            # print('e_max: ' + str(e_max))

            if e_max >= e_max_prev:
                effort += 1
                continue
            break

        # scale e_tot accordingly
        e_tot = pt.overhead * (e_max_prev - e_max) + e_tot_prev
        # print('e_tot: ' + str(e_tot))

        # make all tasks again, this time max pinned to e_max.
        e_list = [e_max] + unifast_divide(opt - 1, e_tot - e_max, e_max)
        e_list.sort(reverse=True)
        # print('e_list_new: ' + str(e_list))

        pt.ts_table[str(opt)] = TaskSet()

        # alpha
        # alpha = (e_tot - e_tot_prev) / (e_max_prev - e_max)
        # print('alpha: ' + str(alpha))
        # print('----------------')

        # update e_tot, e_max
        e_max_prev = e_max
        e_tot_prev = e_tot

        # create threads and append to task set
        ts = TaskSet()

        for i in range(len(e_list)):

            # set minimum e to 1.0
            if e_list[i] < 0.1:
                e_list[i] = 1.0

            thr_param = {
                'id': pt.base_task.id,
                'exec_time': e_list[i],
                'deadline': pt.base_task.deadline,
                'period': pt.base_task.period,
            }
            thr = Thread(**thr_param)

            ts.append(thr)

        # append to pt
        pt.ts_table[str(opt)] = ts
    return


def parallelize_pts_single(pt_list):
    ts = TaskSet()
    for pt in pt_list:
        ts.merge_ts(pt[1])
    return ts


def parallelize_pts_max(pt_list, **kwargs):
    max_opt = kwargs.get('max_option', 1)
    ts = TaskSet()
    for pt in pt_list:
        ts.merge_ts(pt[max_opt])
    return ts


def parallelize_pts_random(pt_list, **kwargs):
    max_opt = kwargs.get('max_option', 1)
    ts = TaskSet()
    for pt in pt_list:
        ts.merge_ts(pt[random.randint(1, max_opt)])
    return ts


def parallelize_pts_custom(pt_list, popt_list):
    if len(pt_list) != len(popt_list):
        raise Exception(
            'pt_list or popt_list malformed. Length does not match.')

    ts = TaskSet()
    for i in range(len(pt_list)):
        ts.merge_ts(pt_list[i][popt_list[i]])
    return ts


def parallelize_multiseg_single(pt_list):
    ts_list = []
    for pt in pt_list:
        ts_list.append(pt[1])
    return ts_list


def parallelize_multiseg_max(pt_list, **kwargs):
    max_opt = kwargs.get('max_option', 1)
    ts_list = []
    for pt in pt_list:
        ts_list.append(pt[max_opt])
    return ts_list


def parallelize_multiseg_random(pt_list, **kwargs):
    max_opt = kwargs.get('max_option', 1)
    ts_list = []
    for pt in pt_list:
        ts_list.append(pt[random.randint(1, max_opt)])
    return ts_list


def parallelize_multiseg_custom(pt_list, popt_list):
    if len(pt_list) != len(popt_list):
        raise Exception(
            'pt_list or popt_list malformed. Length does not match.')
    ts_list = []
    for i, pt in enumerate(pt_list):
        ts_list.append(pt[popt_list[i]])
    # for i in range(len(pt_list)):
    #     ts_list.append(pt_list[i][popt_list[i]])
    return ts_list


if __name__ == '__main__':
    # a = unifast_divide(5, 10, 3)
    # print(a)
    # print(sum(a))
    a = unifast_divide_alpha(2, 100, 70)
    print(a)
    b = normalize_list(a)
    print(b)
    print('---')
    a = unifast_divide_alpha(3, 100, 70)
    print(a)
    b = normalize_list(a)
    print(b)
    print('---')
    a = unifast_divide_alpha(4, 100, 70)
    print(a)
    b = normalize_list(a)
    print(b)
    print('---')
    a = unifast_divide_alpha(5, 100, 70)
    print(a)
    b = normalize_list(a)
    print(b)
    print('---')
