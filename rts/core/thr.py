from rts.core.task import Task


class Thread(Task):
    """
    Class ParaTask : Generate Thread \n

    **Import info :** \n
    +----------------+--------------+
    | Package Name   | Module Name  |
    +================+==============+
    | core           | task         |
    +----------------+--------------+
    """

    cnt = 0

    def __init__(self, **kwargs):
        """
        **Role**: Initialize Thread \n

        .. important:: **thread** inherits from **Task**\n
        Thread = Task + tid. You may treat a thread the same as you would a task.
        """

        super().__init__(**kwargs)
        self.tid = kwargs.get('tid', type(self).cnt)

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
        .. note:: **Thread** => **id** **tid** **exec_time** **deadline** **period**
        """
        return "%d\t%d\t%.2f\t%.2f\t%.2f" % (
            self.id,
            self.tid,
            self.exec_time,
            self.deadline,
            self.period
        )
