import os
from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.op.stat import Stat
from rts.popt.cho import Cho
from rts.op.rt_app import RTApp
from shutil import copyfile

from rts.core.task import Task
from rts.core.pt import ParaTask
from rts.core.ts import TaskSet

if __name__ == '__main__':
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

    # lane tracking tack
    print('----------------')
    print('lane tracking tack')
    task_param = {
        'exec_time': 20,
        'deadline': 50,
        'period': 60,
    }
    t_lanetrack = Task(**task_param)

    para_task_param = {
        'base_task': t_lanetrack,
        'max_option': 4,
        'custom': 'True',
        'exec_times': [[20], [11, 10], [9, 8, 8], [7, 6, 6, 5]],
    }
    pt_lanetrack = ParaTask(**para_task_param)
    print(pt_lanetrack)

    # object detection task
    print('----------------')
    print('object detection task')
    task_param = {
        'exec_time': 30,
        'deadline': 50,
        'period': 60,
    }
    t_objdetect = Task(**task_param)

    para_task_param = {
        'base_task': t_objdetect,
        'max_option': 4,
        'custom': 'True',
        'exec_times': [[30], [17, 15], [12, 12, 10], [9, 8, 8, 7]],
    }
    pt_objdetect = ParaTask(**para_task_param)
    print(pt_objdetect)

    # create pts
    print('----------------')
    print('pts')
    ts = TaskSet()
    ts.append(t_lanetrack)
    ts.append(t_objdetect)

    pts_param_single = {
        'base_ts': ts,
        'max_option': 4,
        'popt_strategy': 'single',
        'custom': 'True',
        'pt_list': [pt_lanetrack, pt_objdetect],
    }

    pts = ParaTaskSet(**pts_param_single)
    pts_util = pts.tot_util()
    print(pts_util)
    print(pts)

    # schedulability check param
    sched_param = {
        'num_core': 4.0,
    }
    bcl_naive = BCLNaive(**sched_param)

    # single thread schedulability
    sched_single = bcl_naive.is_schedulable(pts)
    stat_single.add(pts_util, sched_single)

    print('sched_single: ' + str(sched_single))

    # max thread
    pts.popt_strategy = 'max'
    pts.serialize_pts()

    # max thread schedulability
    sched_max = bcl_naive.is_schedulable(pts)
    stat_max.add(pts_util, sched_max)
    print('sched_max: ' + str(sched_max))

    # random thread
    pts.popt_strategy = 'random'
    pts.serialize_pts()
    rnd_selected_option = pts.popt_list

    # random thread schedulability
    sched_random = bcl_naive.is_schedulable(pts)
    stat_random.add(pts_util, sched_random)
    print('sched_random: ' + str(sched_random))

    pts.popt_strategy = 'custom'
    pts.serialize_pts()

    # cho schedulability
    popt_param = {
        'num_core': 4.0,
        'max_option': 4,
    }
    cho = Cho(**popt_param)
    sched_cho, pts_cho = cho.is_schedulable(pts)
    stat_cho.add(pts_util, sched_cho)
    print('sched_cho: ' + str(sched_cho))
    print('pts_cho: ')
    print(pts_cho)
