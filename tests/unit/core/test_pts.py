from rts.core.pts import ParaTaskSet
from rts.core.thr import Thread

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

    def test_set_thr(self):
        thr_param1 = {
            'id': 0,
        }
        thr1 = Thread(**thr_param1)

        thr_list = []
        thr_list.append(thr1)

        pts = ParaTaskSet()
        pts.append(thr_list)

        thr_param2 = {
            'id': 2,
        }
        thr2 = Thread(**thr_param2)

        pts[0, 0] = thr2

        self.assertEqual(pts[0, 0].id, 2)

    def test_pts_append(self):
        thr_param11 = {
            'id': 0,
        }
        thr11 = Thread(**thr_param11)
        thr_param12 = {
            'id': 1,
        }
        thr12 = Thread(**thr_param12)
        thr_param21 = {
            'id': 2,
        }
        thr21 = Thread(**thr_param21)
        pts = ParaTaskSet()
        pts.append(thr11, 0)
        pts.append(thr12, 0)
        pts.append(thr21, 1)

        self.assertEqual(pts[0, 0].id, 0)
        self.assertEqual(pts[1, 0].id, 2)


if __name__ == '__main__':
    unittest.main()
