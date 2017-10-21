from rts.core.task import Task
from rts.core.taskset import TaskSet
from rts.op import tsutil


def is_schedulable(ts, **kwargs):
    num_core = kwargs.get('num_core', 1)

    lmd_tot = tsutil.sum_density(ts)
    lmd_max = tsutil.max_density(ts)

    sched = lmd_tot <= num_core * (1.0 - lmd_max) + lmd_max
    return sched
