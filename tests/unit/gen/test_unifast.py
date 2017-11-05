import unittest
from rts.gen.unifast import Unifast


class UnifastTestCase(unittest.TestCase):
    """ Tests for `unifast.py`."""

    def test_produces_correct_num_task(self):
        gen_param = {
            'num_task': 10,
        }
        g = Unifast(**gen_param)
        ts = g.next_task_set()

        self.assertEqual(len(ts), 10)


if __name__ == '__main__':
    unittest.main()
