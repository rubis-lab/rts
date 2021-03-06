from rts.core.dag import DAG
from rts.op.tsutil import sum_utilization


class DAGTaskSet(object):
    """
    'DAG Task Set'
    """
    cnt = 0

    def __init__(self, **kwargs):
        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)
        self.popt_strategy = kwargs.get('popt_strategy', 'single')
        self.dags = []

    def __str__(self):
        info_str = ''
        for d in self.dags:
            info_str += d.__str__() + '\n'
        return info_str

    def __len__(self):
        return len(self.dags)

    def __getitem__(self, idx):
        return self.dags[idx]

    def __setitem__(self, idx, val):
        self.dags[idx] = val
        return

    def __iter__(self):
        return iter(self.dags)

    def append(self, d):
        self.dags.append(d)
        return

    def clear(self):
        del self.dags[:]
        return

    def tot_util(self):
        return sum_utilization(self)

    def parallelize_preset(self, preset):
        for dag in self.dags:
            dag.parallelize_preset(preset)
        return
