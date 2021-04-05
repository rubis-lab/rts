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
         * **overhead** : The increasing rate of **execution_time**
         on every **parallelization** \n
         * **variance** : The **execution_time**
         difference between **threads** on parallelization\n
         * **base_task** : **parallelize task** needs **base_task**
         ( Default: exec_time=1, deadline=2, period=3 )\n
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
        self.base_task = kwargs.get('base_task',
            Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))
        ts = TaskSet()
        ts.append(self.base_task)
        self.ts_table = {'1': ts}

        # ts_table
        self.overhead_strategy = kwargs.get('overhead_strategy', 'identical')
        if kwargs.get('custom', 'False') == 'True':
            self.exec_times = kwargs.get('exec_times', [[]])
            self.populate_ts_table_custom()
        elif self.overhead_strategy == 'identical':
            self.populate_ts_table_identical()
        elif self.overhead_strategy == 'linear':
            self.populate_ts_table_linear()
        else:
            self.populate_ts_table()

        # macro
        self.selected_option = 1
        self.selected_tasks = \
            self.ts_table[str(self.selected_option)]
        self.exec_time = self.base_task.exec_time
        self.longest_exec_time = self.base_task.exec_time
        self.total_exec_time = self.base_task.exec_time
        self.deadline = self.base_task.deadline
        self.period = self.base_task.period
        self.configure_pt(self.selected_option)

        # dag specific
        # self.exec_time = float(kwargs.get('exec_time', 0))
        # self.deadline = float(kwargs.get('deadline', 0))
        # self.period = float(kwargs.get('period', 0))
        self.slack = float(kwargs.get('slack', 0))
        self.priority = kwargs.get('priority', -1)
        self.is_dag = kwargs.get('is_dag', False)
        if self.is_dag:
            self.nid = kwargs.get('nid', -1)
            self.pred = kwargs.get('pred', [])
            self.succ = kwargs.get('succ', [])
            self.is_dummy = kwargs.get('is_dummy', False)
            self.start_time = 0.0
            self.finish_time = 0.0

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
         * :py:const:`if opt == 0`
            && :py:const:`if opt < len(self.ts_table)` \n
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
         * :py:const:`if opt == 0`
            && :py:const:`if opt < len(self.ts_table)` \n
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

    def populate_ts_table_identical(self):
        if self.max_opt < 2:
            return

        for opt in range(2, self.max_opt + 1):
            ts = TaskSet()
            thrs = para.parallelize_task_ideal(self.base_task, opt, self.overhead)
            for thr in thrs:
                ts.append(thr)
            self.ts_table[str(opt)] = ts
        return

    def populate_ts_table_linear(self):
        if self.max_opt < 2:
            return

        for opt in range(2, self.max_opt + 1):
            ts = TaskSet()
            thrs = para.parallelize_task_linear(self.base_task, self.max_opt)
            for thr in thrs:
                ts.append(thr)
            self.ts_table[str(opt)] = ts
        return

    def populate_ts_table(self):
        """
        **Role**: Generate **populate_ts_table**
        For more details **See "op.para.parallelize_pt_non_dec_alpha"**
        """

        if self.max_opt >= 2:
            # para.parallelize_pt_non_dec(self)
            para.parallelize_pt_non_dec_alpha(self)
        return

    def configure_pt(self, option):
        self.selected_option = option
        self.selected_tasks = self.ts_table[str(option)]

        self.longest_exec_time = \
            max(list(map(lambda x: x.exec_time, self.selected_tasks)))
        self.total_exec_time = \
            sum(list(map(lambda x: x.exec_time, self.selected_tasks)))
        self.exec_time = self.longest_exec_time

        self.deadline = self.base_task.deadline
        self.period = self.base_task.period
        return

    def increment_option(self):
        if self.selected_option < self.max_opt:
            self.selected_option += 1
            self.configure_pt(self.selected_option)
            return True
        return False
