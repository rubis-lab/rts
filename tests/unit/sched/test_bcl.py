import unittest

from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.sched import bcl


class BCLTestCase(unittest.TestCase):
    """ Tests for `bcl.py`."""

    def test_two_task(self):
        task_param1 = {
            'exec_time': 4,
            'deadline': 10,
            'period': 10,
        }
        t1 = Task(**task_param1)
        task_param2 = {
            'exec_time': 6,
            'deadline': 10,
            'period': 10,
        }
        t2 = Task(**task_param2)
        ts = TaskSet()
        ts.append(t1)
        ts.append(t2)
        bcl_param = {
            'num_core': 2,
        }
        self.assertTrue(bcl.is_schedulable(ts, **bcl_param))

if __name__ == '__main__':
    unittest.main()