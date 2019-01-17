import unittest

from rts.core.task import Task
from rts.core.thr import Thread
from rts.core.pt import ParaTask


class ParaTaskTestCase(unittest.TestCase):
    """ Tests for `pt.py`."""
    def test_init_with_task(self):
        task_param = {
            'exec_time': 4,
            'deadline': 10,
            'period': 10,
        }
        t = Task(**task_param)
        para_task_param = {
            'max_option': 4,
        }
        pt = ParaTask(t, **para_task_param)

        self.assertEqual(pt.max_opt, 4)
        option_one_first_thr = pt.thr_table.get('1')[0]
        self.assertEqual(option_one_first_thr, t)
        self.assertEqual(option_one_first_thr.exec_time, 4)

    def test_append_and_getter(self):
        thr_param11 = {
            'exec_time': 4,
            'deadline': 10,
            'period': 10,
        }
        thr11 = Thread(**thr_param11)
        thr_param21 = {
            'exec_time': 2,
            'deadline': 10,
            'period': 10,
        }
        thr21 = Thread(**thr_param21)
        thr_param22 = {
            'exec_time': 3,
            'deadline': 10,
            'period': 10,
        }
        thr22 = Thread(**thr_param22)

        para_task_param = {
            'max_option': 2,
        }


if __name__ == '__main__':
    unittest.main()