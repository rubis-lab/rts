from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.op import para


class ParaTask(object):

    """
    Class ParaTask : Generate Parallelizable Task\n

    **Import info :** \n
    +----------------+--------------+
    | Package Name   | Module Name  |
    +================+==============+
    | core           | task         |
    +----------------+--------------+
    | core           | ts           |
    +----------------+--------------+
    | op             | para         |
    +----------------+--------------+

    """
    cnt = 0

    def __init__(self, **kwargs):
        """
        **Role**: Initialize Parallelizable Task\n
        .. note::
         * **max_option** : The maximum parallelize option that \n
         * **overhead** : The increasing rate of **execution_time** on every **parallelization** \n
         * **variance** : The **execution_time** difference between **threads** on paralleization\n
         * **base_task** : **parallelize task** needs **base_task** ( Default: exec_time=1, deadline=2, period=3 )\n
         * **ts_table** : Save taskset from **1** to **max_option**\n
         * **populate_ts_table** : See the **"populate_ts_table"**\n

        """

        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)
        self.max_opt = kwargs.get('max_option', 1)

        # parallelizer info
        self.overhead = kwargs.get('overhead', 0.0)
        self.variance = kwargs.get('variance', 0.0)

        # base task info
        self.base_task = kwargs.get('base_task', Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))
        ts = TaskSet()
        ts.append(self.base_task)
        self.ts_table = {'1': ts}

        self.populate_ts_table()

    def __del__(self):
        """
        **Role**: Delete Parallelizable Task
        .. note:: **cnt** : decreases by 1

        """
        type(self).cnt -= 1

    def __str__(self):
        """
        **Role**: Format for printing Parallelizable Task \n

        .. note::
         * **info** = 'id' + 'max_option' + 'base_task'\n
         * :py:const:`if max_option >= 2` \n
            Display **populate_ts_table** for each option
        """

        info = 'id: ' + str(self.id) + '\n' + \
               'max_option: ' + str(self.max_opt) + '\n\n' + \
               'base_task: ' + '\n' + str(self.base_task) + '\n\n'
        if self.max_opt >= 2:
            for i in range(2, self.max_opt + 1):
                info += 'option ' + str(i) + ': \n' + str(self[i]) + '\n'

        return info

    def __len__(self):
        """
        **Role**: Returns max_option**
        """
        return self.max_opt

    # returns task set of option opt
    def __getitem__(self, opt):
        """
        **Role**: Get **ts_table** for given **option**\n
        :param opt: Parallelize Option\n
        .. note::
         * :py:const:`if opt <= len(self.ts_table)` \n
            returns **ts_table** for given option
         * :py:const:`if opt == 0` && :py:const:`if opt < len(self.ts_table)` \n
            Exception Handler
        """

        if opt == 0:
            raise Exception('Parallization option cannot be 0.')
        elif opt <= len(self.ts_table):
            return self.ts_table[str(opt)]
        else:
            raise Exception('Parllelization option out of bound.\n' +
                            'max_parallel option: ' + str(self.max_opt) + '\n' +
                            'requested option: ' + str(opt))

    def __setitem__(self, opt, ts):
        """
        **Role**: Append new **TaskSet** to **ts_table**\n
        :param opt: Parallelize Option\n
        :param ts: TaskSet\n
        .. note::
         * :py:const:`if opt <= len(self.ts_table)` \n
            returns ts_table for given option
         * :py:const:`if opt == 0` && :py:const:`if opt < len(self.ts_table)` \n
            Exception Handler
        """
        if opt == 0:
            raise Exception('Parallization option cannot be 0.')
        elif opt <= len(self.ts_table):
            self.ts_table[str(opt)] = ts
            return
        else:
            raise Exception('Parllelization option out of bound.\n' +
                            'max_parallel option: ' + str(self.max_opt) + '\n' +
                            'requested option: ' + str(opt))

    def populate_ts_table(self):
        """
        **Role**: Generate **populate_ts_table**

        For more details **See "op.para.parallelize_pt_non_dec"**


        """

        ###if self.max_opt >= 2:
        ###    for i in range(2, self.max_opt + 1):
        ###        self.ts_table[str(i)] = TaskSet()
        ###        tlist = para.parallelize_task(self.base_task, **{'pcs': i, 'overhead': self.overhead, 'variance': self.variance})
        ###        for thr in tlist:
        ###            self[i].append(thr)

        if self.max_opt >= 2:
            para.parallelize_pt_non_dec(self)
        return


if __name__ == '__main__':
    task_param = {
        'exec_time': 20,
        'deadline': 60,
        'period': 60,
    }
    t = Task(**task_param)
    para_task_param = {
        'base_task': t,
        'max_option': 4,
        'overhead': 0.1,
        'variance': 0.9,
    }
    pt = ParaTask(**para_task_param)
    print(pt)
