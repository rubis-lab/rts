from tqdm import tqdm
from rts.op.stat import Stat
from rts.popt.cho_mst import ChoMultiSegmentTask
from rts.sched.bcl_mst import BCLMultiSegmentTask
from rts.gen.mstgen import MSgen
from rts.popt.exhaustive_mst import ExhaustiveMultiSegmentTask

# create generator
gen_param = {
    'min_exec_time': 50,
    'max_exec_time': 150,
    'min_period': 100,
    'max_period': 500,
    'min_deadline': 100,
    'max_deadline': 500,
    'tot_util': 4.0,
    'util_over': True,
    'implicit_deadline': False,
    'constrained_deadline': True,
    'min_seg_size': 40,
    'max_seg_size': 100,
    'max_option': 4,
    'overhead': 0.3,
    'variance': 0.7,
    # 'deadline_scale': 0.8
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
stat_cho_fdsf = Stat(**stat_param)
stat_exhaustive = Stat(**stat_param)

# schedulability check param
sched_param = {
    'num_core': 4.0,
}

num_iter = 10000
print_every = 50
for i in tqdm(range(num_iter)):

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
    
    # random thread schedulability
    sched_random = bcl_mst.is_schedulable(msts)
    stat_random.add(msts_util, sched_random)
    
    # cho schedulability (fdsf)
    msts_param = {
        'num_core': 4.0,
        'max_option': 4,
        'inc_strategy': 'fdsf'
    }
    cho_fdsf = ChoMultiSegmentTask(**msts_param)
    sched_cho_fdsf, _ = cho_fdsf.is_schedulable(msts)
    stat_cho_fdsf.add(msts_util, sched_cho_fdsf)

    if sched_cho_fdsf:
        stat_exhaustive.add(msts_util, True)
    else:
        # exhaustive
        exhaustive = ExhaustiveMultiSegmentTask(**{
            'max_option': 3,
            'num_core': 3.0,
            'max_n_seg': 12,
        })
        sched_exhaustive, sched_msts = exhaustive.is_schedulable(msts)
        stat_exhaustive.add(msts_util, sched_exhaustive)


    if i % print_every == 0:
        print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))
        print('single')
        stat_single.print_minimal()
        print('------------')

        print('max')
        stat_max.print_minimal()
        print('------------')

        print('random')
        stat_random.print_minimal()
        print('------------')

        print('cho_fdsf')
        stat_cho_fdsf.print_minimal()
        print('------------')

        print('exhaustive')
        stat_exhaustive.print_minimal()
        print('------------')
