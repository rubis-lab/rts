from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pts import ParaTaskSet

import unittest


class PTSTestCase(unittest.TestCase):
    """ Tests for `pts.py`."""

    def test_single_and_max_popt(self):
        task_param = {
            'exec_time': 4,
            'deadline': 10,
            'period': 10,
        }
        t1 = Task(**task_param)

        task_param = {
            'exec_time': 10,
            'deadline': 20,
            'period': 20,
        }
        t2 = Task(**task_param)

        ts = TaskSet()
        ts.append(t1)
        ts.append(t2)

        pts_param1 = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.0,
            'variance': 0.3,
            'popt': 'single',
        }
        pts1 = ParaTaskSet(**pts_param1)
        self.assertEqual(len(pts1), 2)

        pts_param2 = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.0,
            'variance': 0.3,
            'popt': 'max',
        }
        pts2 = ParaTaskSet(**pts_param2)
        self.assertEqual(len(pts2), 8)


if __name__ == '__main__':
    unittest.main()
