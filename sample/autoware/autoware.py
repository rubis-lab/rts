import os
import yaml
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from rts.op.stat import Stat
from rts.gen.dgen import Dgen
from rts.sched.chwa_dag import ChwaDAG
from rts.popt.cho_dag import ChoDAGTask


if __name__ == '__main__':
    cfg_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'cfg.yaml')
    with open(cfg_file, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    dg = Dgen(**cfg['dgen'])
    stat_base = Stat(**cfg['stat'])
    stat_max = Stat(**cfg['stat'])
    stat_cho = Stat(**cfg['stat'])

    chwa = ChwaDAG(**cfg['chwa_dag'])
    cho_dag = ChoDAGTask(**cfg['cho_dag'])

    # create tasks with specified params

    # check single is false

    # check max is false

    # check ours is true

    # output parallel options

    for _ in tqdm(range(cfg['num_iter'])):
        dagts = dg.next_task_set()
        dag_util = dagts.tot_util()

        # base (chwa) (single)
        stat_base.add(dag_util, chwa.is_schedulable(dagts))

        # max
        dagts.parallelize_preset('max')
        stat_max.add(dag_util, chwa.is_schedulable(dagts))

        # cho
        dagts.parallelize_preset('single')
        stat_cho.add(dag_util, cho_dag.is_schedulable(dagts))

    print('base')
    base_res, base_res_str = stat_base.result_minimal()
    print(base_res_str)
    print('------------')

    print('max')
    max_res, max_res_str = stat_max.result_minimal()
    print(max_res_str)
    print('------------')

    print('cho')
    cho_res, cho_res_str = stat_cho.result_minimal()
    print(cho_res_str)
    print('------------')

    x_max = 4.0
    y_max = 1.0
    x = list(np.arange(0, 4.0, 0.1))
    # print('x({}): {}'.format(len(x), x))
    # print('base_res({}): {}'.format(len(base_res), base_res))
    plt.plot(x, base_res,
        'ko-',
        label='single',
        markerfacecolor='none',
        linewidth=0.5)

    plt.plot(x, max_res,
        'ks-',
        label='max',
        markerfacecolor='none',
        linewidth=0.5)

    plt.plot(x, cho_res,
        'kx-',
        label='ours',
        markerfacecolor='none',
        linewidth=0.5)

    plt.xlabel('Task Set Utilization')
    plt.ylabel('Schedulability')
    plt.legend(edgecolor='none')
    # plt.axis([0, x_max, 0, y_max])

    plt.show()
