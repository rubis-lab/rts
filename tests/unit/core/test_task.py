import unittest
from rts.core.task import Task


class TaskTestCase(unittest.TestCase):
    """ Tests for `task.py`."""
    def test_id_does_not_overlap(self):
        t1 = Task()
        t2 = Task()
        self.assertNotEqual(t1.id, t2.id)

    def test_task_created_as_specified(self):
        param = {'exec_time': 1, 'deadline': 2, 'period': 3}
        param2 = {'exec_time': 1, 'deadline': 2, 'period': 3}
        t1 = Task(**param)
        self.assertEqual(t1.exec_time, 1)
        t2 = Task(**param2)
        self.assertEqual(t2.deadline, 2)


if __name__ == '__main__':
    unittest.main()
