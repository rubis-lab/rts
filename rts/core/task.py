class Task(object):
    'Basic task class'
    cnt = 0

    def __init__(self, **kwargs):

        self.id = kwargs.get('id', type(self).cnt)
        self.exec_time = kwargs.get('exec_time', 0)
        self.deadline = kwargs.get('deadline', 0)
        self.period = kwargs.get('period', 0)

        for key, value in kwargs.items():
            setattr(self, key, value)

        type(self).cnt += 1

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        """
        return str(self.id)
        + "\t" + str(self.period)
        + "\t" + str(self.exec_time)
        + "\t" + str(self.deadline)
        """
        return "%d\t%.2f\t%.2f\t%.2f" % (
            self.id,
            self.exec_time,
            self.deadline,
            self.period)
"""
param = {'exec_time': 1, 'deadline': 2, 'period': 3}

t1 = Task(**param)
print(t1)
#t2 = Task(4.0, 5, 6)
#print(t1)
#print(t2)
"""
