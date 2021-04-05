from rts.popt.popt import Popt
import math
from rts.op.log import new_logger
from rts.sched.chwa_dag import ChwaDAG


class ChoDAGTask(Popt):
    'Cho DAG Task'

    def __init__(self, **kwargs):
        self.log = new_logger(__name__)
        self.max_opt = kwargs.get('max_option', 1)
        self.num_core = float(kwargs.get('num_core', 1.0))
        self.chwa = ChwaDAG(**{'num_core': self.num_core})
        return

    def __del__(self):
        return

    def __str__(self):
        info = ''
        return info

    def is_schedulable(self, dagts):
        updated = True
        while updated:
            updated = False

            # already done in dag.py
            # for dag in dagts:
            #     assign_priority(dag)

            for base_dag in dagts:
                interference = self.chwa.sum_interference(dagts, base_dag)
                tolerance = self.chwa.sum_tolerance(base_dag)
                if interference > tolerance:
                    # try incrementing dag
                    if base_dag.increment_fdf():
                        updated = True
                    else:
                        return False  # unschedulable
        return True
