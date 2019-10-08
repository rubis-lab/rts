from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.op import para
from rts.core.thr import Thread


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
         * **variance** : The **execution_time** difference between **threads** on parallelization\n
         * **base_task** : **parallelize task** needs **base_task** ( Default: exec_time=1, deadline=2, period=3 )\n
         * **ts_table** : Save taskset from **1** to **max_option**\n
         * **populate_ts_table** : See the **"populate_ts_table"**\n
        """

        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)
        self.max_opt = kwargs.get('max_option', 1)

        # parallelizer info
        self.overhead = kwargs.get('overhead', 0.0)
        self.variance = kwargs.get('variance', 1.0)

        # base task info
        self.base_task = kwargs.get('base_task', Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))
        ts = TaskSet()
        ts.append(self.base_task)
        self.ts_table = {'1': ts}

        if kwargs.get('custom', 'False') == 'True':
            self.exec_times = kwargs.get('exec_times', [[]])
            self.populate_ts_table_custom()
        else:
            self.populate_ts_table()

    def populate_ts_table_custom(self):
        """
        **Role**: Populate ts_table using predefined execution times.\n
        """
        if self.max_opt >= 2:
            # para.parallelize_pt_non_dec_alpha(self)
            for opt in range(1, self.max_opt + 1):

                ts = TaskSet()
                for i in range(0, opt):

                    thr_param = {
                        'id': self.base_task.id,
                        'exec_time': self.exec_times[opt - 1][i],
                        'deadline': self.base_task.deadline,
                        'period': self.base_task.period,
                    }
                    thr = Thread(**thr_param)

                    ts.append(thr)
                self.ts_table[str(opt)] = ts
        return

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
            raise Exception('Parallelization option cannot be 0.')
        elif opt <= len(self.ts_table):
            return self.ts_table[str(opt)]
        else:
            raise Exception('Parallelization option out of bound.\n' +
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
            raise Exception('Parallelization option cannot be 0.')
        elif opt <= len(self.ts_table):
            self.ts_table[str(opt)] = ts
            return
        else:
            raise Exception('Parallelization option out of bound.\n' +
                            'max_parallel option: ' + str(self.max_opt) + '\n' +
                            'requested option: ' + str(opt))

    def populate_ts_table(self):
        """
        **Role**: Generate **populate_ts_table**
        For more details **See "op.para.parallelize_pt_non_dec_alpha"**
        """

        if self.max_opt >= 2:
            # para.parallelize_pt_non_dec(self)
            para.parallelize_pt_non_dec_alpha(self)
        return
