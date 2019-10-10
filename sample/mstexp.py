from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.op.stat import Stat
from rts.popt.cho import Cho
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
    stat_base = Stat(**stat_param)

    notify_every = 100
    num_iter = 1000

    # schedulability check param
    sched_param = {
        'num_core': 4.0,
    }

    for i in range(num_iter):

        if i % notify_every == 0:
            print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))

        # generate tasks
        msts = msg.next_mst_set()

        # configure ms (not used now).
        # ms_param_single = {
        #     'base_ts': ts,
        #     'max_option': 4,
        #     'overhead': 0.3,
        #     'variance': 0.7,
        #     'popt_strategy': 'single',
        # }

        msts_util = msts.tot_util()

        # check schedulability
        bcl_mst = BCLMultiSegmentTask(**sched_param)
        sched_base = bcl_mst.is_schedulable(msts)
        stat_base.add(msts_util, sched_base)

    print("base")
    stat_base.print_minimal()
    print("------------")

