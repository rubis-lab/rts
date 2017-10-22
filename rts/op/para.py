from rts.core.thr import Thread

import random
import operator


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
    a = 0 	.. b = Ck
    
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
