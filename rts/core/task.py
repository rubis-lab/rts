from rts.op import tsutil


class Task(object):
    """
    Class Task : Generate Basic Task\n

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
        **Role**: Make **Task** instances based on keyword argument\n
        **Example**: \n
        Task = {id : cnt , exec_time : 0, deadline : 0, period : 0}\n
        .. note:: **cnt** : increases by 1
        """
        self.id = kwargs.get('id', type(self).cnt)
        self.exec_time = float(kwargs.get('exec_time', 0))
        self.deadline = float(kwargs.get('deadline', 0))
        self.period = float(kwargs.get('period', 0))
        self.slack = float(kwargs.get('slack', 0))
        type(self).cnt += 1

    def __del__(self):
        """
        **Role**: Delete Class
        .. note:: **cnt** : decreases by 1
        """
        type(self).cnt -= 1

    def __str__(self):
        """
        **Role**: Format for printing **Task** instance(s)\n
        id    exec_time    deadline    period
        """
        ret = "%d\t%.2f\t%.2f\t%.2f" % (
            self.id,
            self.exec_time,
            self.deadline,
            self.period
        )
        return ret

    def utilization(self):
        """
        **Role**: Returns Utilization\n
        .. note:: **utilization**  **=** **exec_time** / **period**\t
        ( from  **"op.tsutil.calc_utilization"**  )
        """
        return tsutil.calc_utilization(self)
