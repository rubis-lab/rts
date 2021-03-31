import math
from rts.sched.sched import Sched
from rts.op.log import new_logger
from rts.core.dag import DAG
from rts.core.dagts import DAGTaskSet


class ChwaDAG(Sched):
    def __init__(self, **kwargs):
        self.num_core = float(kwargs.get('num_core', 1.0))
        self.log = new_logger(__name__)

    def sum_interference(self, dagts, base_dag):
        w_other = 0.0
        for inter_dag in dagts:
            if inter_dag == base_dag:
                continue
            w_other += inter_dag.workload_gedf(base_dag.deadline)
        w_self = base_dag.graph_vol() - base_dag.graph_len()

        return w_other + w_self

    def is_schedulable(self, dagts):
        for base_dag in dagts:
            interference = self.sum_interference(dagts, base_dag)
            tolerance = self.num_core * \
                (base_dag.deadline - base_dag.graph_len())
            if interference > tolerance:
                return False
        return True


if __name__ == '__main__':
    from rts.gen.dgen import Dgen
    dg = Dgen(**{
        'min_period': 60,
        'max_period': 200,
        'min_nodes': 1,
        'max_nodes': 10,
        'edge_prob': 0.3,
        'util_over': True,
        'avg_node_util': 0.15,
        'num_task': 3
    })
    dagts = dg.next_task_set()

    chwa = ChwaDAG(**{'num_core': 4.0})
    print(chwa.is_schedulable(dagts))
