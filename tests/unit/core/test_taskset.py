import unittest
from rts.core.task import Task
from rts.core.taskset import TaskSet


class TaskSetTestCase(unittest.TestCase):
    """ Tests for `task.py`."""

    def test_id_does_not_overlap(self):
        param = {}
        ts1 = TaskSet(**param)
        ts2 = TaskSet(**param)
        self.assertNotEqual(ts1.id, ts2.id)

    def test_task_is_counted(self):
        param = {}
        ts = TaskSet(**param)
        t1 = Task(**param)
        t2 = Task(**param)
        ts.append(t1)
        ts.append(t2)
        self.assertEqual(len(ts), 2)

    def test_taskset_is_cleared(self):
        param = {}
        ts = TaskSet(**param)
        t1 = Task(**param)
        ts.append(t1)
        ts.clear()
        self.assertEqual(len(ts), 0)

if __name__ == '__main__':
    unittest.main()
