import unittest

from rts.core.thr import Thread
from rts.core.pts import ParaTaskSet
from rts.sched import bcl_mod


class BCLTestCase(unittest.TestCase):
    """ Tests for `bcl.py`."""

    def test_two_thread(self):
        thread_param1 = {
            'id': 11,
            'exec_time': 4,
            'deadline': 10,
            'period': 10,
        }
        t1 = Thread(**thread_param1)
        thread_param2 = {
            'id': 12,
            'exec_time': 2,
            'deadline': 10,
            'period': 10,
        }
        t2 = Thread(**thread_param2)
        thread_param3 = {
            'id': 21,
            'exec_time': 2,
            'deadline': 10,
            'period': 10,
        }
        t3 = Thread(**thread_param3)

        pts = ParaTaskSet()
        pts.append(t1, 0)
        pts.append(t2, 0)
        pts.append(t3, 1)
        bcl_mod_param = {
            'num_core': 2,
        }
        self.assertTrue(bcl_mod.is_schedulable(pts, **bcl_mod_param))


if __name__ == '__main__':
    unittest.main()
