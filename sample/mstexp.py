from rts.op.stat import Stat
from rts.popt.cho_mst import ChoMultiSegmentTask
from rts.sched.bcl_mst import BCLMultiSegmentTask
from rts.gen.mstgen import MSgen

if __name__ == '__main__':
    # create generator
    gen_param = {
        'min_exec_time': 50,
        'max_exec_time': 120,
        'min_period': 80,
        'max_period': 250,
        'min_deadline': 80,
        'max_deadline': 250,
        'tot_util': 4.0,
        'util_over': True,
        'implicit_deadline': False,
        'constrained_deadline': True,
        'min_seg_size': 15,
        'max_seg_size': 40,
        'max_option': 4
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
    stat_cho = Stat(**stat_param)

    notify_every = 1
    num_iter = 1

    # schedulability check param
    sched_param = {
        'num_core': 4.0,
    }

    for i in range(num_iter):

        if i % notify_every == 0:
            print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))
        print('--------')
        # generate tasks
        msts = msg.next_mst_set()
        msts_util = msts.tot_util()
        print(msts)
        print('--------')
        # check schedulability
        bcl_mst = BCLMultiSegmentTask(**sched_param)
        sched_single = bcl_mst.is_schedulable(msts)
        stat_single.add(msts_util, sched_single)

        # cho schedulability
        msts_param = {
            'num_core': 4.0,
            'max_option': 4,
        }
        cho = ChoMultiSegmentTask(**msts_param)
        sched_cho, _ = cho.is_schedulable(msts)
        stat_cho.add(msts_util, sched_cho)

    # print("single")
    # stat_single.print_minimal()
    # print("------------")
    #
    # print("cho")
    # stat_cho.print_minimal()
    # print("------------")
