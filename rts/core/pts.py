class ParaTaskSet(object):
    'Parallelizable Task Set'
    cnt = 0

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', type(self).cnt)
        self.thr_list = []

        type(self).cnt += 1

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        return "%d\t" % (
            self.id)

    def __len__(self):
        return len(self.thr_list)

    def __getitem__(self, idx):
        t_idx, thr_idx = idx
        return self.thr_list[t_idx][thr_idx]

    def __setitem__(self, idx, val):
        self.thr_list[idx] = val
        return

    def __iter__(self):
        return iter(self.thr_list)

    def append(self, t):
        self.thr_list.append(t)
        return

    def clear(self):
        del self.thr_list[:]
        return
