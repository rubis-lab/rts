class ParaTaskSet(object):
    'Parallelizable Task Set'
    cnt = 0

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', type(self).cnt)
        self.thr_list_seq = []
        self.thr_cnt = [0]

        type(self).cnt += 1

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        return "%d\t" % (
            self.id)

    def __len__(self):
        return len(self.thr_list_seq)

    def __getitem__(self, idx):
        return self.thr_list_seq[self.thr_cnt[idx]:self.thr_cnt[idx + 1]]

    def __iter__(self):
        return iter(self.thr_list_seq)

    def shift_thr_cnt_right(self, t_idx):
        for curr_t_idx in range(len(self.thr_cnt)):
            if curr_t_idx > t_idx:
                self.thr_cnt[curr_t_idx] += 1
        return

    def shift_thr_cnt_left(self, t_idx):
        for curr_t_idx in range(len(self.thr_cnt)):
            if curr_t_idx > t_idx:
                self.thr_cnt[curr_t_idx] -= 1
        return

    def append(self, t, t_idx=-1):
        # insert list of items
        if t_idx < 0:
            self.thr_list_seq[len(self.thr_list_seq):] = t
            self.thr_cnt.append(self.thr_cnt[-1] + len(t))

        # insert single item
        else:
            # if sibling thread already exist in list
            if t_idx + 1 < len(self.thr_cnt):
                self.thr_list_seq.insert(self.thr_cnt[t_idx + 1], t)
                self.shift_thr_cnt_right(t_idx)

            # if sibling thread not in list
            else:
                self.thr_list_seq.append(t)
                while t_idx + 1 > len(self.thr_cnt):
                    self.thr_cnt.append(self.thr_cnt[-1])
                self.thr_cnt.append(self.thr_cnt[-1] + 1)

    def clear(self):
        del self.thr_list_seq[:]
        return
