from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.op import tsutil

import unittest
from nose.tools import assert_almost_equals


class TSUtilTestCase(unittest.TestCase):
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

    def test_workload_in_interval_edf(self):
        task_param = {
            'exec_time': 3,
            'deadline': 5,
            'period': 7,
        }
        t = Task(**task_param)
        t.slack = 0
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 2.0), 2.0)
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 4.0), 3.0)

        t.slack = 1
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 2.0), 1.0)
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 9.0), 4.0)
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 10.0), 5.0)

        t.slack = 2
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 9.0), 3.0)

    def test_workload_in_interval_edf_wo_slack(self):
        task_param = {
            'exec_time': 3,
            'deadline': 5,
            'period': 7,
        }
        t = Task(**task_param)
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 9.0), 5.0)
        assert_almost_equals(tsutil.workload_in_interval_edf(t, 10.0), 6.0)

    def test_workload_in_interval_fp(self):
        task_param = {
            'exec_time': 3,
            'deadline': 5,
            'period': 7,
        }
        t = Task(**task_param)
        assert_almost_equals(tsutil.workload_in_interval_fp(t, 14.0), 8.0)
        assert_almost_equals(tsutil.workload_in_interval_fp(t, 15.0), 9.0)
        assert_almost_equals(tsutil.workload_in_interval_fp(t, 2.0), 2.0)
        assert_almost_equals(tsutil.workload_in_interval_fp(t, 4.0), 3.0)

        t.slack = 1
        assert_almost_equals(tsutil.workload_in_interval_fp(t, 15.0), 8.0)
        assert_almost_equals(tsutil.workload_in_interval_fp(t, 16.0), 9.0)


if __name__ == '__main__':
    unittest.main()
