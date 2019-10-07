from rts.core.task import Task
from rts.core.pt import ParaTask
from rts.op import para

import unittest

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

        self.assertAlmostEqual(thr_list[0].exec_time, 5.0)
        self.assertAlmostEqual(thr_list[1].exec_time, 5.0)

        self.assertAlmostEqual(thr_list[0].deadline, 10.0)
        self.assertAlmostEqual(thr_list[0].period, 10.0)

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

        self.assertAlmostEqual(thr_list[0].exec_time, 10.0)
        self.assertAlmostEqual(thr_list[1].exec_time, 10.0)

    def test_overhead_calculation_for_pt(self):
        task_param = {
            'exec_time': 200,
            'deadline': 600,
            'period': 600,
        }
        t = Task(**task_param)
        para_task_param = {
            'base_task': t,
            'max_option': 4,
            'overhead': 0.1,
            'variance': 0.9,
        }
        pt = ParaTask(**para_task_param)
        





if __name__ == '__main__':
    unittest.main()
