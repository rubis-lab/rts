from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCL_Naive
from rts.op.stat import Stat
from rts.popt.cho import Cho


if __name__ == '__main__':
    # create generator
    gen_param = {
        'num_task': 10,
        'min_exec_time': 30,
        'max_exec_time': 100,
        'min_period': 60,
        'max_period': 200,
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
    stat_random = Stat(**stat_param)
    stat_cho = Stat(**stat_param)

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
            'overhead': 0.1,
            'variance': 0.8,
            'popt_strategy': 'single',
        }
        pts = ParaTaskSet(**pts_param_single)
        pts_util = pts.tot_util()

        # single thread schedulability
        bcl_naive = BCL_Naive(**sched_param)
        sched_single = bcl_naive.is_schedulable(pts)
        stat_single.add(pts_util, sched_single)

        # max thread
        pts.popt_strategy = 'max'
        pts.serialize_pts()

        # max thread schedulability
        sched_max = bcl_naive.is_schedulable(pts)
        stat_max.add(pts_util, sched_max)

        # random thread
        pts.popt_strategy = 'random'
        pts.serialize_pts()

        # random thread schedulability
        sched_random = bcl_naive.is_schedulable(pts)
        stat_random.add(pts_util, sched_random)

        pts.popt_strategy = 'single'
        pts.serialize_pts()

        # cho
        pts.popt_strategy = 'custom'
        pts.serialize_pts()

        # cho schedulability
        popt_param = {
            'num_core': 4.0,
            'max_option': 4,
        }

        cho = Cho(**popt_param)
        sched_cho = cho.is_schedulable(pts)
        stat_cho.add(pts_util, sched_cho)

        if not sched_cho:
            if sched_single or sched_max or sched_random:
                print('!!something wrong')
                print(pts)
            if sched_single:
                print('sched_single')
            if sched_max:
                print('sched_max')
            if sched_random:
                print('sched_random')

    print("single")
    stat_single.print_minimal()
    print("------------")

    print("max")
    stat_max.print_minimal()
    print("------------")

    print("random")
    stat_random.print_minimal()
    print("------------")

    print("cho")
    stat_cho.print_minimal()
    print("------------")
