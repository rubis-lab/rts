from rts.op import tsutil


class TaskSet(object):
    """
    Class ParaTask : Generate TaskSet\n

    **Import info :** \n
    +----------------+--------------+
    | Package Name   | Module Name  |
    +================+==============+
    | op             | tsutil       |
    +----------------+--------------+

    """

    cnt = 0

    def __init__(self, **kwargs):
        """
        **Role**: Initialize **id (= cnt) & task_list** based on keyword argument\n

        .. note:: **cnt** : increases by 1

        """
        self.id = kwargs.get('id', type(self).cnt)
        self.task_list = []

        type(self).cnt += 1

    def __del__(self):
        """
        **Role**: Delete Class\n
        .. note:: **cnt** : decreases by 1
        """
        type(self).cnt -= 1

    def __str__(self):
        """
        **Role**: Format for printing taskset \n

        length of task_list, tot_util

        .. note:: **tot_util** : sum of each task's utilization (from **"op.tsutil.sum_utilization"**)
        """

        tot_util = tsutil.sum_utilization(self)

        info_str = '%d\t%.2f\n' % (
            len(self.task_list),
            tot_util)

        for t in self.task_list:
            info_str += t.__str__() + '\n'

        return info_str

    def __len__(self):
        """
        **Role**: Returns length of **task_list**
        """

        return len(self.task_list)

    def __getitem__(self, idx):
        """
        **Role**: Get **Task** based on index
        """
        return self.task_list[idx]

    def __setitem__(self, idx, val):
        """
        **Role**: Set **Task** value with given variable
        """
        self.task_list[idx] = val
        return

    def __iter__(self):
        """
        **Role**: Set **Task** value with given variable
        """
        return iter(self.task_list)

    def append(self, t):
        """
        **Role**: Append **Task** to **task_list**
        """
        self.task_list.append(t)
        return

    def clear(self):
        """
        **Role**: Delete **Task** from **task_list**
        """
        del self.task_list[:]
        return

    def tot_util(self):
        """
        **Role**: Calculate total utilization (from **"op.tsutil.sum_utilization"**)
        """
        return tsutil.sum_utilization(self)

    def merge_ts(self, ts):
        """
        **Role**: Merge 2 **task_lists** to in 1 **task_list**
        """
        self.task_list += ts.task_list
        return self

