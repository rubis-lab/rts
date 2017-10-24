from rts.core.pts import ParaTaskSet
from rts.core.thr import Thread
from rts.core.task import Task

import unittest


class PTSTestCase(unittest.TestCase):
    """ Tests for `pts.py`."""
    def test_thr_added(self):
        thr11 = Thread()
        thr12 = Thread()

        thr_list1 = []
        thr_list1.append(thr11)
        thr_list1.append(thr12)

        thr21 = Thread()
        thr_list2 = []
        thr_list2.append(thr21)

        pts = ParaTaskSet()
        pts.append(thr_list1)
        pts.append(thr_list2)

        self.assertEqual(len(pts), 2)

    def test_get_thr(self):
        thr11 = Thread()
        thr12 = Thread()

        thr_list1 = []
        thr_list1.append(thr11)
        thr_list1.append(thr12)

        thr21 = Thread()
        thr_list2 = []
        thr_list2.append(thr21)

        pts = ParaTaskSet()
        pts.append(thr_list1)
        pts.append(thr_list2)
        self.assertNotEqual(pts[0, 0].id, pts[1, 0].id)


if __name__ == '__main__':
    unittest.main()
