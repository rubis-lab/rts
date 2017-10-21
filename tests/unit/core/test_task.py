import unittest
from rts.core.task import Task


class TaskTestCase(unittest.TestCase):
    """ Tests for `task.py`."""
    def test_id_does_not_overlap(self):
        t1 = Task()
        t2 = Task()
        self.assertNotEqual(t1.id, t2.id)

if __name__ == '__main__':
    unittest.main()
