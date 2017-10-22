import unittest
from rts.core.task import Task
from rts.core.ts import TaskSet


class TaskSetTestCase(unittest.TestCase):
    """ Tests for `taskset.py`."""

    def test_id_does_not_overlap(self):
        ts1 = TaskSet()
        ts2 = TaskSet()
        self.assertNotEqual(ts1.id, ts2.id)

    def test_task_is_counted(self):
        ts = TaskSet()
        t1 = Task()
        t2 = Task()
        ts.append(t1)
        ts.append(t2)
        self.assertEqual(len(ts), 2)

    def test_taskset_is_cleared(self):
        ts = TaskSet()
        t1 = Task()
        ts.append(t1)
        ts.clear()
        self.assertEqual(len(ts), 0)

    def test_task_getter(self):
        ts = TaskSet()
        param = {'id': 2}
        t = Task(**param)
        ts.append(t)
        self.assertEqual(ts[0].id, 2)

    def test_task_setter(self):
        ts = TaskSet()
        param1 = {'id': 2}
        t1 = Task(**param1)
        ts.append(t1)
        param2 = {'id': 3}
        t2 = Task(**param2)
        ts[0] = t2
        self.assertEqual(ts[0].id, 3)

if __name__ == '__main__':
    unittest.main()
