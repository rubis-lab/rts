from rts.op.stat import Stat

import unittest


class StatTestCase(unittest.TestCase):
    """ Tests for `stat.py`."""

    def test_idx_calc(self):
        stat_param = {
            'id': 0,
            'min': 1.0,
            'max': 2.1,
        }
        s = Stat(**stat_param)

        self.assertEqual(s.conv_idx(1.24), 2)
        self.assertEqual(s.conv_idx(1.25), 2)

    def test_proportion_calc(self):
        stat_param = {
            'id': 0,
            'min': 0.0,
            'max': 2.1,
        }
        s = Stat(**stat_param)
        s.add(0.1, True)
        s.add(0.1, True)
        s.add(0.1, True)
        s.add(0.1, False)
        s.add(0.1, True)
        s.normalize()
        self.assertAlmostEqual(s.norm_data[s.conv_idx(0.1)], 0.8)


if __name__ == '__main__':
    unittest.main()
