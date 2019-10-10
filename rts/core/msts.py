from rts.op import tsutil


class MultiSegmentTaskSet(object):
    cnt = 0

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', type(self).cnt)
        self.mst_list = []
        type(self).cnt += 1

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        info_str = '%d\t%.2f\n' % (
            len(self.mst_list),
            self.tot_util())

        for t in self.mst_list:
            info_str += t.__str__() + '\n'

        return info_str

    def __len__(self):
        return len(self.mst_list)

    def __getitem__(self, idx):
        return self.mst_list[idx]

    def __setitem__(self, idx, val):
        self.mst_list[idx] = val
        return

    def __iter__(self):
        return iter(self.mst_list)

    def append(self, t):
        self.mst_list.append(t)
        return

    def clear(self):
        del self.mst_list[:]
        return

    def tot_util(self):
        return tsutil.sum_utilization(self)


