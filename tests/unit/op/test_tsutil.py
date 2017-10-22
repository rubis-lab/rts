import unittest
from nose.tools import assert_almost_equals

from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.op import tsutil


class TsutilTestCase(unittest.TestCase):
    """ Tests for `tsutil.py`."""

    def test_max_density(self):
        task_param1 = {
            'exec_time': 8,
            'deadline': 10,
        }
        t1 = Task(**task_param1)
        task_param2 = {
            'exec_time': 9,
            'deadline': 10,
        }
        t2 = Task(**task_param2)
        ts = TaskSet()
        ts.append(t1)
        ts.append(t2)
        assert_almost_equals(tsutil.max_density(ts), 0.9)

    def test_sum_density(self):
        task_param1 = {
            'exec_time': 8,
            'deadline': 10,
        }
        t1 = Task(**task_param1)
        task_param2 = {
            'exec_time': 9,
            'deadline': 10,
        }
        t2 = Task(**task_param2)
        ts = TaskSet()
        ts.append(t1)
        ts.append(t2)
        assert_almost_equals(tsutil.sum_density(ts), 1.7)

    def test_utilization_and_density_difference(self):
        task_param = {
            'exec_time': 6,
            'deadline': 8,
            'period': 10,
        }
        t = Task(**task_param)
        ts = TaskSet()
        ts.append(t)
        diff = tsutil.sum_utilization(ts) - tsutil.sum_density(ts)
        assert_almost_equals(diff, -0.15)

if __name__ == '__main__':
    unittest.main()
