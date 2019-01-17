from rts.gen.unifast import Unifast
from rts.sched import bcl_naive
from rts.op.stat import Stat
from rts.op import tsutil

if __name__ == '__main__':
    # create generator
    gen_param = {
        'num_task': 8,
        'min_exec_time': 30,
        'max_exec_time': 80,
        'min_period': 20,
        'max_period': 60,
        'tot_util': 4.0,
    }
    u = Unifast(**gen_param)
    print(u)
    print('--------')


    stat_param = {
        'id': 0,
        'min': 0.0,
        'max': 4.0,
        'inc': 0.1,
    }
    stat_single = Stat(**stat_param)
    stat_random = Stat(**stat_param)
    stat_para = Stat(**stat_param)



    num_iter = 10000
    for i in range(num_iter):
        # generate tasks
        ts = u.next_task_set()
        # print(ts)

        # test using various tests
        sched_param = {
            'num_core': 4.0,
        }
        sched_single = bcl_naive.is_schedulable(ts, **sched_param)
        #sched_gfb = gfb.is_schedulable(ts, **sched_param)
        #sched_bcl_mod = bcl_mod.is_schedulable(ts, **sched_param)

        ts_util = tsutil.sum_utilization(ts)
        stat_single.add(ts_util, sched_single)
        #stat_bcl.add(ts_util, sched_bcl)
        #stat_bcl_mod.add(ts_util, sched_bcl_mod)

        #print('single- ' + str(sched_single))
        # print('bcl- ' + str(sched_bcl))
        # print('bcl_mod- ' + str(sched_bcl_mod))
        # print('--------')

    print("single")
    stat_single.print_minimal()
    print("------------")
"""
    print("bcl")
    stat_bcl.print_minimal()
    print("------------")

    print("bcl_mod")
    stat_bcl_mod.print_minimal()
    print("------------")
"""