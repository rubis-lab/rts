from rts.op.stat import Stat
from rts.popt.cho_mst import ChoMultiSegmentTask
from rts.sched.bcl_mst import BCLMultiSegmentTask
from rts.gen.mstgen import MSgen

if __name__ == '__main__':
    # create generator
    gen_param = {
        'min_exec_time': 50,
        'max_exec_time': 150,
        'min_period': 100,
        'max_period': 300,
        'min_deadline': 100,
        'max_deadline': 300,
        'tot_util': 4.0,
        'util_over': True,
        'implicit_deadline': False,
        'constrained_deadline': True,
        'min_seg_size': 30,
        'max_seg_size': 80,
        'max_option': 4,
        'overhead': 0.3,
        'variance': 0.7
    }
    msg = MSgen(**gen_param)
    print(msg)

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

    notify_every = 10000
    num_iter = 100000

    # schedulability check param
    sched_param = {
        'num_core': 4.0,
    }

    for i in range(num_iter):
        if i % notify_every == 0:
            print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))

        # generate tasks
        msts = msg.next_mst_set()
        msts_util = msts.tot_util()
        # print(msts)

        # single thread schedulability
        bcl_mst = BCLMultiSegmentTask(**sched_param)
        sched_single = bcl_mst.is_schedulable(msts)
        stat_single.add(msts_util, sched_single)

        # max thread
        msts.popt_strategy = 'max'
        msts.update_msts()

        # max thread schedulability
        sched_max = bcl_mst.is_schedulable(msts)
        stat_max.add(msts_util, sched_max)

        # random thread
        msts.popt_strategy = 'random'
        msts.update_msts()
        # rnd_selected_option = pts.popt_list

        # random thread schedulability
        sched_random = bcl_mst.is_schedulable(msts)
        stat_random.add(msts_util, sched_random)

        # cho schedulability
        msts_param = {
            'num_core': 4.0,
            'max_option': 4,
        }
        cho = ChoMultiSegmentTask(**msts_param)
        sched_cho, _ = cho.is_schedulable(msts)
        stat_cho.add(msts_util, sched_cho)

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