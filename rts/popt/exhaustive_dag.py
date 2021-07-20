from rts.popt.popt import Popt
import math
from rts.op.log import new_logger
from rts.sched.chwa_dag import ChwaDAG

class ExhaustiveDAGTask(Popt):
    'Exhaustive DAG Task'

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

    def conv_num_base(self, n, b, idx):
        if n == 0:
            return idx
        i = 0
        while n > 0:
            idx[i] = int(n % b)
            i += 1
            n //= b
        return idx

    def is_schedulable(self, dagts):
        # number of possible cases: max_opt ^ n_task
        n_task = 0
        res = False
        for dag in dagts:
            n_task += len(dag.tasks) -2

        # print(str(n_task)+"      1111111111111111111")
        
        # print("maxopt:" + str(self.max_opt))
        for i in range(self.max_opt ** n_task):
            idx = [0 for j in range(n_task)]
            self.conv_num_base(i, self.max_opt, idx)
            # print(idx)

            it = 0
            for dag in dagts:
                for task in dag:
                    if not task.is_dummy:
                        task.configure_pt(idx[it]+1)
                        it += 1

            
            # print(str(it)+"      222222222222222")

            tempres = True
            for base_dag in dagts:
                interference = self.chwa.sum_interference(dagts, base_dag)
                tolerance = self.chwa.sum_tolerance(base_dag)
                if interference > tolerance:
                    tempres = False
            
            if tempres:
                res = tempres
                break
        

        return res
                
    # def is_schedulable(self, dagts):

    #     updated = True
    #     while updated:
    #         updated = False

    #         # already done in dag.py
    #         # for dag in dagts:
    #         #     assign_priority(dag)

    #         for base_dag in dagts:
    #             interference = self.chwa.sum_interference(dagts, base_dag)
    #             tolerance = self.chwa.sum_tolerance(base_dag)
    #             if interference > tolerance:
    #                 # try incrementing dag
    #                 if base_dag.increment_fdf():
    #                     updated = True
    #                 else:
    #                     return False  # unschedulable
    #     return True
