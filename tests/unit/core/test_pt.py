import unittest

from rts.core.task import Task
from rts.core.thr import Thread
from rts.core.pt import ParaTask


class ParaTaskTestCase(unittest.TestCase):
    """ Tests for `pt.py`."""
    def test_init_with_task(self):
        task_param = {
            'exec_time': 40,
            'deadline': 100,
            'period': 100,
        }
        t = Task(**task_param)
        para_task_param = {
            'base_task': t,
            'max_option': 4,
        }
        pt = ParaTask(**para_task_param)

        self.assertEqual(pt.max_opt, 4)
        option_one_first_thr = pt[1][0]
        self.assertEqual(option_one_first_thr, t)
        self.assertEqual(option_one_first_thr.exec_time, 40)

    def test_get_set_item_raise_error(self):
        task_param = {
            'exec_time': 40,
            'deadline': 100,
            'period': 100,
        }
        t = Task(**task_param)
        para_task_param = {
            'base_task': t,
            'max_option': 4,
        }
        pt = ParaTask(**para_task_param)
        with self.assertRaises(Exception):
            temp_val = pt[5]
        with self.assertRaises(Exception):
            temp_val += pt[0]
        with self.assertRaises(Exception):
            pt[5] = temp_val

    def test_custom_populate(self):
        task_param = {
            'exec_time': 20,
            'deadline': 50,
            'period': 60,
        }
        t = Task(**task_param)
        para_task_param = {
            'base_task': t,
            'max_option': 4,
            'custom': 'True',
            'exec_times': [[20], [11, 10], [9, 8, 8], [7, 6, 6, 5]],
        }
        pt = ParaTask(**para_task_param)
        ts4 = pt[4]
        self.assertEqual(ts4[0].exec_time, 7)
        self.assertEqual(ts4[1].deadline, 50)
        self.assertEqual(ts4[2].period, 60)
        self.assertEqual(ts4[3].exec_time, 5)


if __name__ == '__main__':
    unittest.main()
