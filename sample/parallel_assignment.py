#from rts.gen.ugen import Ugen
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

    # log stat
    stat_param = {
        'id': 0,
        'min': 0.0,
        'max': 4.0,
        'inc': 0.1,
    }
    stat_naive = Stat(**stat_param)

    num_iter = 10000
    for i in range(num_iter):
        # generate tasks
        ts = u.next_task_set()
        if ts == -1:
            print("error")

        # test using various tests
        sched_param = {
            'num_core': 4.0,
        }
        sched_naive = bcl_naive.is_schedulable(ts, **sched_param)

        ts_util = tsutil.sum_utilization(ts)
        stat_naive.add(ts_util, sched_naive)

    print("naive")
    stat_naive.print_minimal()
    print("------------")