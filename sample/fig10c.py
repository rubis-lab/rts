from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.op.stat import Stat
from rts.popt.cho import Cho
from rts.sched import bcl

if __name__ == '__main__':
    # create generator
    gen_param = {
        'min_exec_time': 30,
        'max_exec_time': 100,
        'min_period': 60,
        'max_period': 200,
        'min_deadline': 40,
        'max_deadline': 200,
        'tot_util': 4.0,
        'util_over': True,
        'implicit_deadline': False,
        'constrained_deadline': True,
        'deadline_scale': 0.8,
    }
    u = Egen(**gen_param)
    print(u)

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

    notify_every = 1000
    num_iter = 10000

    # schedulability check param
    sched_param = {
        'num_core': 4.0,
    }

    for i in range(num_iter):

        if i % notify_every == 0:
            print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))
            
        # generate tasks
        ts = u.next_task_set()

        # configure pts
        pts_param_single = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.3,
            'variance': 0.7,
            'popt_strategy': 'single',
        }
        pts = ParaTaskSet(**pts_param_single)
        pts_util = pts.tot_util()

        # single thread schedulability
        bcl_naive = BCLNaive(**sched_param)
        sched_single = bcl_naive.is_schedulable(ts)
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
        rnd_selected_option = pts.popt_list

        # random thread schedulability
        sched_random = bcl_naive.is_schedulable(pts)
        stat_random.add(pts_util, sched_random)

        # cho
        pts.popt_strategy = 'custom'
        pts.serialize_pts()

        # cho schedulability
        popt_param = {
            'num_core': 4.0,
            'max_option': 4,
        }

        cho = Cho(**popt_param)
        sched_cho, _ = cho.is_schedulable(pts)
        stat_cho.add(pts_util, sched_cho)

    print("single")
    stat_single.print_minimal()
    print("------------")
    
    print("max")
    stat_max.print_minimal()
    print("------------")
    
    print("random")
    stat_random.print_minimal()
    print("------------")
    
    print("ours")
    stat_cho.print_minimal()
    print("------------")
    
