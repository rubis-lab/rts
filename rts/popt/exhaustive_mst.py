from rts.popt.popt import Popt
from rts.sched.sched import Sched
from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pts import ParaTaskSet
from rts.sched.bcl_naive import BCLNaive


class ExhaustiveMultiSegmentTask(Popt):
    'Exhaustive search'

    def __init__(self, **kwargs):
        self.max_opt = kwargs.get('max_option', 1)
        self.sched = kwargs.get('sched', Sched())
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
        while n:
            idx[i] = int(n % b)
            i += 1
            n //= b
        return idx

    def is_schedulable(self, msts):
        # total number of segments
        tot_n_seg = 0
        for mst in msts:
            tot_n_seg += len(mst)

        if tot_n_seg > 15:
            print('tot_n_seg')
            print(tot_n_seg)

        for i in range(self.max_opt ** tot_n_seg):
            idx = [0 for _ in range(tot_n_seg)]
            idx_conv = self.conv_num_base(i, self.max_opt, idx)

            for mst in msts:
                idx_mst = idx_conv[:len(mst)]
                idx_conv_left = idx_conv[len(mst):]
                idx_conv = idx_conv_left


            # set parallel option



        # # number of possible cases: max_opt ^ (sum n_seg)
        # n_seg
        # n_task = len(pts.base_ts)
        # for i in range(self.max_opt ** n_task):
        #     idx = [0 for j in range(n_task)]
        #     self.conv_num_base(i, self.max_opt, idx)
        #
        #     # set parallel option
        #     for j in range(n_task):
        #         pts.popt_list[j] = idx[j] + 1
        #     pts.serialize_pts()
        #
        #     # check schedulability
        #     if self.sched.is_schedulable(pts):
        #         return True
        #
        # return False

    def get_opt_popt(self, pts):
        pass


if __name__ == '__main__':
    ex = ExhaustiveMultiSegmentTask(**{
        'max_option': 4,
    })
    idx = [0 for _ in range(8)]
    idx_conv = ex.conv_num_base(14215, 4, idx)
    print('idx_conv')
    print(idx_conv)

    for _ in range(4):
        idx_used = idx_conv[:2]
        idx_left = idx_conv[2:]
        print('idx_used')
        print(idx_used)
        print('idx_left')
        print(idx_left)
        idx_conv = idx_left
    # task_param = {
    #     'exec_time': 4,
    #     'deadline': 10,
    #     'period': 10,
    # }
    # t1 = Task(**task_param)
    #
    # task_param = {
    #     'exec_time': 10,
    #     'deadline': 20,
    #     'period': 20,
    # }
    # t2 = Task(**task_param)
    #
    # ts = TaskSet()
    # ts.append(t1)
    # ts.append(t2)
    #
    # pts_param = {
    #     'base_ts': ts,
    #     'max_option': 2,
    #     'overhead': 0.0,
    #     'variance': 0.3,
    #     'popt_strategy': 'custom',
    #     'popt_list': [1, 1],
    # }
    #
    # pts = ParaTaskSet(**pts_param)
    # print(pts)
    #
    # sched_param = {
    #     'num_core': 1.0,
    # }
    # bcl_naive = BCL_Naive(**sched_param)
    #
    # popt_param = {
    #     'max_option': 2,
    #     'sched':bcl_naive,
    # }
    # exhaustive = Exhaustive(**popt_param)
    #
    # ss = exhaustive.is_schedulable(pts)
    # print('Exhaustive test result:')
    # print(ss)
