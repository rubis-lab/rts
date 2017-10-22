import unittest
from rts.gen.gen import Gen


class GenTestCase(unittest.TestCase):
    """ Tests for `gen.py`."""

    def test_produces_correct_num_task(self):
        gen_param = {
            'num_task': 10,
        }
        g = Gen(**gen_param)
        ts = g.next_task_set()

        self.assertEqual(len(ts), 10)

    def test_correct_exec_time_range(self):
        gen_param = {
            'num_task': 1,
            'min_exec_time': 0,
            'max_exec_time': 10,
        }
        g = Gen(**gen_param)
        ts = g.next_task_set()

        self.assertTrue(ts[0].exec_time <= 10)
        self.assertTrue(ts[0].exec_time >= 0)

if __name__ == '__main__':
    unittest.main()
