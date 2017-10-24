from rts.core.task import Task
from rts.op import para

import unittest
from nose.tools import assert_almost_equals


class ParaTestCase(unittest.TestCase):
    """ Tests for `para.py`."""

    def test_split_into_two(self):
        task_param = {
            'exec_time': 10,
            'deadline': 10,
            'period': 10,
        }
        t = Task(**task_param)

        para_param = {
            'pcs': 2,
            'overhead': 0.0,
            'variance': 0.0,
        }
        thr_list = para.parallelize_task(t, **para_param)

        assert_almost_equals(thr_list[0].exec_time, 5.0)
        assert_almost_equals(thr_list[1].exec_time, 5.0)

        assert_almost_equals(thr_list[0].deadline, 10.0)
        assert_almost_equals(thr_list[0].period, 10.0)

    def test_overhead_calculation(self):
        task_param = {
            'exec_time': 10,
            'deadline': 10,
            'period': 10,
        }
        t = Task(**task_param)

        para_param = {
            'pcs': 2,
            'overhead': 1.0,
            'variance': 0.0,
        }

        thr_list = para.parallelize_task(t, **para_param)

        assert_almost_equals(thr_list[0].exec_time, 10.0)
        assert_almost_equals(thr_list[1].exec_time, 10.0)


if __name__ == '__main__':
    unittest.main()
