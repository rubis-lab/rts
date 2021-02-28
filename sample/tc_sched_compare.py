from tqdm import tqdm
from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.sched.bcl import BCL
from rts.sched.bar import BAR
from rts.op.stat import Stat
from rts.popt.cho import Cho
import tikzplotlib
import numpy as np
import matplotlib.pyplot as plt
from rts.popt.exhaustive import Exhaustive


# create generator
# gen_param = {
#     'min_exec_time': 30,
#     'max_exec_time': 100,
#     'min_period': 60,
#     'max_period': 200,
#     'min_deadline': 40,
#     'max_deadline': 200,
#     'tot_util': 4.0,
#     'util_over': True,
#     'implicit_deadline': False,
#     'constrained_deadline': True,
# }
gen_param = {
    'min_exec_time': 15,
    'max_exec_time': 35,
    'min_period': 20,
    'max_period': 65,
    'min_deadline': 15,
    'max_deadline': 65,
    'tot_util': 4.0,
    'util_over': True,
    'implicit_deadline': False,
    'constrained_deadline': True,
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
stat_bcl = Stat(**stat_param)
stat_rta = Stat(**stat_param)
stat_bar = Stat(**stat_param)
stat_cho = Stat(**stat_param)
stat_rta_exhaustive = Stat(**stat_param)
stat_bar_exhaustive = Stat(**stat_param)

# schedulability check param
sched_param = {
    'num_core': 4.0,
}

bcl_naive = BCLNaive(**sched_param)
rta = BCL(**sched_param)
bar = BAR(**sched_param)
rta_exhastive = Exhaustive(**{
    'max_option': 4,
    'sched': rta
})
bar_exhastive = Exhaustive(**{
    'max_option': 4,
    'sched': bar
})
num_iter = 500
for i in tqdm(range(num_iter)):
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

    # bcl naive schedulability
    sched_bcl = bcl_naive.is_schedulable(ts)
    stat_bcl.add(pts_util, sched_bcl)

    # rta schedulability
    sched_rta = rta.is_schedulable(ts)
    stat_rta.add(pts_util, sched_rta)

    # bar schedulability
    sched_bar = bar.is_schedulable(ts)
    stat_bar.add(pts_util, sched_bar)

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

    if sched_cho:
        stat_rta_exhaustive.add(pts_util, True)
        stat_bar_exhaustive.add(pts_util, True)
    else:
        pts.popt_strategy = 'single'
        pts.serialize_pts()

        # rta_exhaust schedulability
        sched_rta_exhaustive = rta_exhastive.is_schedulable(pts)
        stat_rta_exhaustive.add(pts_util, sched_rta)

        # bar_exhaust schedulability
        sched_bar_exhaustive = bar_exhastive.is_schedulable(pts)
        stat_bar_exhaustive.add(pts_util, sched_bar)


log_file = 'tc_log.txt'
r = ''
r += 'bcl\n'
r_bcl, r_str = stat_bcl.result_minimal()
r += r_str + '------------\n'

r += 'rta\n'
r_rta, r_str = stat_rta.result_minimal()
r += r_str + '------------\n'

r += 'bar\n'
r_bar, r_str = stat_bar.result_minimal()
r += r_str + '------------\n'

r += 'cho\n'
r_cho, r_str = stat_cho.result_minimal()
r += r_str + '------------\n'

r += 'rta_exhaustive\n'
r_rta_exhaustive, r_str = stat_rta_exhaustive.result_minimal()
r += r_str + '------------\n'

r += 'bar_exhaustive\n'
r_bar_exhaustive, r_str = stat_bar_exhaustive.result_minimal()
r += r_str + '------------\n'

# save to file
with open(log_file, 'w') as f:
    f.write(r)

# plot
x = np.arange(0, 4, 0.1)
plt.plot(x, r_bcl,
    'ko-',
    label='bcl',
    markerfacecolor='none',
    linewidth=0.5)

plt.plot(x, r_rta,
    'k^-',
    label='rta',
    markerfacecolor='none',
    linewidth=0.5)

plt.plot(x, r_bar,
    'ks-',
    label='bar',
    markerfacecolor='none',
    linewidth=0.5)

plt.plot(x, r_cho,
    'kx-',
    label='cho',
    markerfacecolor='none',
    linewidth=0.5)

plt.plot(x, r_rta_exhaustive,
    'k+-',
    label='rta_exhaustive',
    markerfacecolor='none',
    linewidth=0.5)

plt.plot(x, r_bar_exhaustive,
    'k*-',
    label='bar_exhaustive',
    markerfacecolor='none',
    linewidth=0.5)

plt.xlabel('Task Set Utilization')
plt.ylabel('Schedulability')
plt.legend(edgecolor='none')
plt.axis([0.0, 4.0, 0, 1.0])

out_tex = 'tc_sched_compare.tex'
tikzplotlib.save(out_tex)

plt.show()
