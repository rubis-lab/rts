from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCL_Naive
from rts.op.stat import Stat

if __name__ == '__main__':
    # create generator
    gen_param = {
        'num_task': 10,
        'min_exec_time': 1,
        'max_exec_time': 30,
        'min_period': 30,
        'max_period': 60,
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
    stat_max = Stat(**stat_param)
    stat_max_vs_single = Stat(**stat_param)
    stat_random = Stat(**stat_param)
    stat_random_vs_single = Stat(**stat_param)

    num_iter = 1000
    for i in range(num_iter):
        # generate tasks
        ts = u.next_task_set()
        if ts == -1:
            print("error")

        # schedulability check param
        sched_param = {
            'num_core': 4.0,
        }

        # single thread
        pts_param_single = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.0,
            'variance': 0.3,
            'popt': 'single',
        }
        pts_single = ParaTaskSet(**pts_param_single)

        # single thread schedulability
        bcl_naive = BCL_Naive(**sched_param)
        sched_single = bcl_naive.is_schedulable(pts_single)
        stat_single.add(pts_single.tot_util(), sched_single)

        # max thread
        pts_param_max = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.0,
            'variance': 0.3,
            'popt': 'max',
        }
        pts_max = ParaTaskSet(**pts_param_max)

        # max thread schedulability
        sched_max = bcl_naive.is_schedulable(pts_max)
        stat_max.add(pts_max.tot_util(), sched_max)
        stat_max_vs_single.add(pts_single.tot_util(), sched_max)

        # random thread
        pts_param_random = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.0,
            'variance': 0.3,
            'popt': 'random',
        }
        pts_random = ParaTaskSet(**pts_param_random)

        # random thread schedulability
        sched_random = bcl_naive.is_schedulable(pts_random)
        stat_random.add(pts_random.tot_util(), sched_random)
        stat_random_vs_single.add(pts_single.tot_util(), sched_random)

    print("single")
    stat_single.print_minimal()
    print("------------")

    print("max")
    stat_max.print_minimal()
    print("------------")

    print("random")
    stat_random.print_minimal()
    print("------------")

    print("max_vs_single")
    stat_max_vs_single.print_minimal()
    print("------------")

    print("random_vs_single")
    stat_random_vs_single.print_minimal()
    print("------------")