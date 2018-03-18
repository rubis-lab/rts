from rts.gen.unifast import Unifast
from rts.sched import gfb, bcl, bcl_mod
from rts.op.stat import Stat
from rts.op import tsutil

if __name__ == '__main__':
    # create generator
    gen_param = {
        'num_task': 3,
        'min_exec_time': 2,
        'max_exec_time': 7,
        'min_period': 2,
        'max_period': 7,
        'tot_util': 2.0,
    }
    u = Unifast(**gen_param)
    # print(u)
    # print('--------')
    stat_param = {
        'id': 0,
        'min': 0.0,
        'max': 4.0,
        'inc': 0.1,
    }
    stat_gfb = Stat(**stat_param)
    stat_bcl = Stat(**stat_param)
    stat_bcl_mod = Stat(**stat_param)

    num_iter = 10000
    for i in range(num_iter):
        # generate tasks
        ts = u.next_task_set()
        # print(ts)

        # test using various tests
        sched_param = {
            'num_core': 2,
        }
        sched_bcl = bcl.is_schedulable(ts, **sched_param)
        sched_gfb = gfb.is_schedulable(ts, **sched_param)
        sched_bcl_mod = bcl_mod.is_schedulable(ts, **sched_param)

        ts_util = tsutil.sum_utilization(ts)
        stat_gfb.add(ts_util, sched_gfb)
        stat_bcl.add(ts_util, sched_bcl)
        stat_bcl_mod.add(ts_util, sched_bcl_mod)

        if not sched_bcl and sched_bcl_mod:
            print(ts)

        # print('gfb- ' + str(sched_gfb))
        # print('bcl- ' + str(sched_bcl))
        # print('bcl_mod- ' + str(sched_bcl_mod))
        # print('--------')
"""
    print("gfb")
    stat_gfb.print_minimal()
    print("------------")

    print("bcl")
    stat_bcl.print_minimal()
    print("------------")

    print("bcl_mod")
    stat_bcl_mod.print_minimal()
    print("------------")
"""