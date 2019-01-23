from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.op import para

class ParaTask(object):
    'Parallelizable Task Set'
    cnt = 0

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', type(self).cnt)
        self.max_opt = kwargs.get('max_option', 1)

        self.base_task = kwargs.get('base_task', Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))
        ts = TaskSet()
        ts.append(self.base_task)
        self.ts_table = {
            '1': ts
        }
        type(self).cnt += 1
        self.populate_ts_table()

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        info = 'id: ' + str(self.id) + '\n' + \
               'max_option: ' + str(self.max_opt) + '\n\n' + \
               'base_task: ' + '\n' + str(self.base_task) + '\n\n'
        if self.max_opt >= 2:
            for i in range(2, self.max_opt + 1):
                info += 'option ' + str(i) + ': \n' + str(self[i]) + '\n'

        return info

    def __len__(self):
        return self.max_opt

    # returns task set of option opt
    def __getitem__(self, opt):
        if opt == 0:
            raise Exception('Parallization option cannot be 0.')
        elif opt <= len(self.ts_table):
            return self.ts_table[str(opt)]
        else:
            raise Exception('Parllelization option out of bound.\n' +
                            'max_parallel option: ' + str(self.max_opt) + '\n' +
                            'requested option: ' + str(opt))

    def __setitem__(self, opt, ts):
        if opt == 0:
            raise Exception('Parallization option cannot be 0.')
        elif opt <= len(self.ts_table):
            self.ts_table[str(opt)] = ts
            print('sss')
            return
        else:
            raise Exception('Parllelization option out of bound.\n' +
                            'max_parallel option: ' + str(self.max_opt) + '\n' +
                            'requested option: ' + str(opt))

    def append(self, opt, ts):
        pass

    def populate_ts_table(self):
        if self.max_opt >= 2:
            for i in range(2, self.max_opt + 1):
                self.ts_table[str(i)] = TaskSet()
                tlist = para.parallelize_task(self.base_task, **{'pcs': i})
                for thr in tlist:
                    self[i].append(thr)

        return

if __name__ == '__main__':
    task_param = {
        'exec_time': 4,
        'deadline': 10,
        'period': 10,
    }
    t = Task(**task_param)
    para_task_param = {
        'base_task': t,
        'max_option': 4,
    }
    pt = ParaTask(**para_task_param)
    print(pt)