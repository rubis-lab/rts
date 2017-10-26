class ParaTaskSet(object):
    'Parallelizable Task Set'
    cnt = 0

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', type(self).cnt)
        self.thr_list = []
        self.thr_list_seq = self.thr_list

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
        t_idx, thr_idx = idx
        self.thr_list[t_idx][thr_idx] = val
        return

    def __iter__(self):
        return iter(self.thr_list_seq)

    def __next__(self):

        return

    def append(self, t, t_idx=-1):
        # adding thread list
        if t_idx < 0:
            self.thr_list.append(t)
        # adding single thread at a time
        else:
            while len(self.thr_list) <= t_idx:
                self.thr_list.append([])
            self.thr_list[t_idx].append(t)
        return

    def clear(self):
        del self.thr_list[:]
        return
