from rts.core.pts import ParaTaskSet
from rts.core.thr import Thread

import unittest


class PTSTestCase(unittest.TestCase):
    """ Tests for `pts.py`."""

    def test_get_thr(self):
        thr11 = Thread()
        thr12 = Thread()

        thr_list1 = []
        thr_list1.append(thr11)
        thr_list1.append(thr12)

        thr_param21 = {
            'id': 2,
        }
        thr21 = Thread(**thr_param21)
        thr_list2 = []
        thr_list2.append(thr21)

        pts = ParaTaskSet()
        pts.append(thr_list1)
        pts.append(thr_list2)
        self.assertNotEqual(pts[0][0].id, pts[1][0].id)
        self.assertEqual(pts[1][0].id, 2)

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

        self.assertEqual(pts[0][0].id, 0)
        self.assertEqual(pts[0][1].id, 1)
        self.assertEqual(pts[1][0].id, 2)

    def test_pts_seq_list_iterator(self):
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

        idx = 0
        for thr in pts:
            if idx == 2:
                self.assertEqual(thr.id, 2)
            idx += 1


if __name__ == '__main__':
    unittest.main()
