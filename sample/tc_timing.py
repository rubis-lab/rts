from tqdm import tqdm
from rts.op.stat import Stat
from rts.popt.cho_mst import ChoMultiSegmentTask
from rts.sched.bcl_mst import BCLMultiSegmentTask
from rts.gen.mstgen import MSgen
import time
import tikzplotlib
import numpy as np
import matplotlib.pyplot as plt

# create generator
gen_param = {
    'min_exec_time': 50,
    'max_exec_time': 150,
    'min_period': 100,
    'max_period': 2000,
    'min_deadline': 100,
    'max_deadline': 2000,
    'tot_util': 4.0,
    'util_over': True,
    'implicit_deadline': False,
    'constrained_deadline': True,
    'min_seg_size': 20,
    'max_seg_size': 80,
    'max_option': 4,
    'overhead': 0.3,
    'variance': 0.7,
    'deadline_scale': 0.8
}
msg = MSgen(**gen_param)
print(msg)

# logger
stat_cho_fdsf = Stat(**{
    'id': 0,
    'min': 0.0,
    'max': 4.0,
    'inc': 0.1,
})

stat_time = Stat(**{
    'id': 1,
    'min': 0.0,
    'max': 50.0,
    'inc': 1.0,
    'mode': 'float'
})

# schedulability check param
sched_param = {
    'num_core': 4.0,
}

num_iter = 100000
times = []
lengths = []
for i in tqdm(range(num_iter)):

    # generate tasks
    msts = msg.next_mst_set()
    msts_util = msts.tot_util()
    # print(msts)

    # cho schedulability (fdsf)
    msts_param = {
        'num_core': 4.0,
        'max_option': 4,
        'inc_strategy': 'fdsf'
    }

    cho_fdsf = ChoMultiSegmentTask(**msts_param)
    t0 = time.perf_counter()
    sched_cho_fdsf, _ = cho_fdsf.is_schedulable(msts)
    t1 = time.perf_counter()
    times.append(t1 - t0)
    lengths.append(len(msts))

    stat_time.add(len(msts), 1000 * (t1 - t0))
    stat_cho_fdsf.add(msts_util, sched_cho_fdsf)

print('cho_fdsf')
_, r_cho = stat_cho_fdsf.result_minimal()
print(r_cho)
print('------------')

print('time')
t_avg = 1000 * sum(times) / len(times)
print('{} ms'.format(t_avg))

print('length')
l_avg = sum(lengths) / len(lengths)
print('{} tasks'.format(l_avg))

print('stat_time')
r_time, r_time_str = stat_time.result_minimal()
print(r_time_str)
print('------------')

# plot
x_max = 20
y_max = 7
x = [int(i + 1) for i in range(x_max)]
plt.plot(x, r_time[:x_max],
    'ko-',
    # label='bcl',
    markerfacecolor='none',
    linewidth=0.5)

plt.xlabel('Number of tasks')
plt.ylabel('Average time spent (ms)')
plt.legend(edgecolor='none')
plt.axis([0, x_max, 0, y_max])
plt.xticks(range(1, x_max + 1))
plt.yticks(range(0, y_max + 1))

out_tex = 'tc_timing.tex'
tikzplotlib.save(out_tex)

plt.show()