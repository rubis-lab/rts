import math
from rts.sched.sched import Sched


class ChwaDAG(Sched):
    def __init__(self, **kwargs):
        self.num_core = float(kwargs.get('num_core', 1.0))

    def is_schedulable(self, ts):
        return True
