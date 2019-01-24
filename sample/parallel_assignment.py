from rts.core.pt import ParaTask
from rts.gen.egen import Egen
from rts.sched import bcl_naive
from rts.op.stat import Stat
from rts.op import tsutil

if __name__ == '__main__':
    # create generator
    gen_param = {
        'num_task': 10,
        'min_exec_time': 1,
        'max_exec_time': 30,
        'min_period': 50,
        'max_period': 100,
        'tot_util': 4.0,
    }
    u = Egen(**gen_param)
    print(u)
    print('--------')

    # logger
    stat_param = {
        'id': 0,
        'min': 0.0,
        'max': 4.0,
        'inc': 0.1,
    }
    stat_single = Stat(**stat_param)
    stat_random = Stat(**stat_param)

    num_iter = 10000
    for i in range(num_iter):
        # generate tasks
        ts = u.next_task_set()
        if ts == -1:
            print("error")

        # single thread
        sched_param = {
            'num_core': 4.0,
        }
        sched_single = bcl_naive.is_schedulable(ts, **sched_param)

        # multiple thread
        # todo

        ts_util = tsutil.sum_utilization(ts)
        stat_single.add(ts_util, sched_single)

    print("single")
    stat_single.print_minimal()
    print("------------")