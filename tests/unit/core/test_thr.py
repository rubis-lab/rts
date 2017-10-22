import unittest
from rts.core.thr import Thread


class TaskTestCase(unittest.TestCase):
    """ Tests for `thread.py`."""
    def test_id_and_tid_does_not_overlap(self):
        t1 = Thread()
        t2 = Thread()
        self.assertNotEqual(t1.id, t2.id)
        self.assertNotEqual(t1.tid, t2.tid)


if __name__ == '__main__':
    unittest.main()
