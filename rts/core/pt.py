from rts.core.task import Task


class ParaTask(object):
    'Parallelizable Task Set'
    cnt = 0

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', type(self).cnt)
        self.max_opt = kwargs.get('max_option', 1)
        self.thr_set_table = {
            '1': [kwargs.get('base_task', Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))]
        }
        type(self).cnt += 1

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        return

    def __len__(self):
        return

    def __getitem__(self, opt):
        if opt == 0:
            return
        if opt <= len(self.thr_set_table):
            return self.thr_set_table[str(opt)]

    def __setitem__(self, opt, thrs):
        return

    def append(self, opt, thrs):
        pass

    def populate_thr_set_table(self):
        pass


if __name__ == '__main__':
    task_param = {
        'exec_time': 1,
        'deadline': 2,
        'period': 3
    }
    t1 = Task(**task_param)
    print(t1)

    pt_param = {
        'base_task': t1,
        'max_option': 4,
    }
    a1 = ParaTask(**pt_param)
    print(a1.cnt)
    print(a1.id)
    # get first task from option 1
    print(a1[1][0].exec_time)
    """
    a2 = ParaTask()
    print(a1.cnt)

    print(a2.cnt)
    print(ParaTask.cnt)
    print(a2.id)
    """
