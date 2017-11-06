from rts.gen.unifast import Unifast
from rts.sched import gfb, bcl, bcl_mod

if __name__ == '__main__':
    # create generator
    gen_param = {
        'num_task': 5,
        'min_exec_time': 1,
        'max_exec_time': 10,
        'min_period': 1,
        'max_period': 10,
        'tot_util': 2.0,
    }
    u = Unifast(**gen_param)
    print(u)
    print('--------')

    num_iter = 5
    for i in range(num_iter):
        # generate tasks
        ts = u.next_task_set()
        print(ts)

        # test using various tests
        sched_param = {
            'num_core': 4,
        }
        sched_bcl = bcl.is_schedulable(ts, **sched_param)
        sched_gfb = gfb.is_schedulable(ts, **sched_param)
        sched_bcl_mod = bcl_mod.is_schedulable(ts, **sched_param)
        print('gfb- ' + str(sched_gfb))
        print('bcl- ' + str(sched_bcl))
        print('bcl_mod- ' + str(sched_bcl_mod))
        print('--------')
