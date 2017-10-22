from rts.core.task import Task


class Thread(Task):
    'Thread class inherited from Task'
    cnt = 0

    def __init__(self, **kwargs):
        super(type(self), self).__init__(**kwargs)
        self.tid = kwargs.get('tid', type(self).cnt)

        type(self).cnt += 1

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        return "%d\t%d\t%.2f\t%.2f\t%.2f" % (
            self.id,
            self.tid,
            self.exec_time,
            self.deadline,
            self.period
        )
