from tqdm import tqdm
from rts.op.stat import Stat
from rts.gen.dgen import Dgen
from rts.sched.chwa_dag import ChwaDAG
import numpy as np
import matplotlib.pyplot as plt
from rts.popt.cho_dag import ChoDAGTask


if __name__ == '__main__':
    dg = Dgen(**{
        'min_period': 60,
        'max_period': 200,
        'min_nodes': 3,
        'max_nodes': 10,
        'edge_prob': 0.3,
        'util_over': True,
        'avg_node_util': 0.15,
        'num_task': 3,
        'max_option': 4,
        'para_strategy': 'linear',
        'overhead': 0.3,
        'variance': 0.1,
    })
    print(dg)

    stat_param = {
        'id': 0,
        'min': 0.0,
        'max': 4.0,
        'inc': 0.1,
    }
    stat_base = Stat(**stat_param)
    stat_cho = Stat(**stat_param)

    chwa = ChwaDAG(**{'num_core': 4.0})
    cho_dag = ChoDAGTask(**{'num_core': 4.0})

    num_iter = 2000
    for _ in tqdm(range(num_iter)):
        dagts = dg.next_task_set()
        dag_util = dagts.tot_util()

        # base (chwa)
        stat_base.add(dag_util, chwa.is_schedulable(dagts))

        # cho
        stat_cho.add(dag_util, cho_dag.is_schedulable(dagts))

    print('base')
    base_res, base_res_str = stat_base.result_minimal()
    print(base_res_str)
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
        label='base',
        markerfacecolor='none',
        linewidth=0.5)

    plt.plot(x, cho_res,
        'kx-',
        label='cho',
        markerfacecolor='none',
        linewidth=0.5)

    plt.xlabel('Task Set Utilization')
    plt.ylabel('Schedulability')
    # plt.legend(edgecolor='none')
    # plt.axis([0, x_max, 0, y_max])

    plt.show()
