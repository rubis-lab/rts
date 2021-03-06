from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.mst import MultiSegmentTask

import unittest


class MultiSegmentTaskTestCase(unittest.TestCase):
	""" Tests for `mst.py`."""

	def test_default_multiseg_created(self):
		ms = MultiSegmentTask()
		self.assertEqual(ms[0][0].exec_time, 1.0)
		self.assertEqual(ms[0][0].deadline, 2.0)

	def test_multiple_segment_created(self):
		t1 = Task(**{
			'exec_time': 20,
			'deadline': 30,
			'period': 40
		})
		t2 = Task(**{
			'exec_time': 40,
			'deadline': 60,
			'period': 80
		})
		ts = TaskSet()
		ts.append(t1)
		ts.append(t2)

		ms = MultiSegmentTask(**{
			'base_ts': ts,
			'max_option': 4,
			'popt_strategy': 'single'
		})

		self.assertEqual(len(ms), 2)
		self.assertEqual(ms[1][0].exec_time, 40)
		self.assertEqual(len(ms[1]), 1)

	def test_parallelization_change(self):
		t1 = Task(**{
			'exec_time': 20,
			'deadline': 30,
			'period': 40
		})
		t2 = Task(**{
			'exec_time': 40,
			'deadline': 60,
			'period': 80
		})
		ts = TaskSet()
		ts.append(t1)
		ts.append(t2)

		ms = MultiSegmentTask(**{
			'base_ts': ts,
			'max_option': 4,
			'popt_strategy': 'single'
		})

		ms.popt_strategy = 'max'
		ms.update_ts_list()
		self.assertEqual(len(ms), 2)
		self.assertEqual(len(ms[0]), 4)
		self.assertEqual(len(ms[1]), 4)

	def test_task_like_property(self):
		t1 = Task(**{
			'exec_time': 20,
			'deadline': 30,
			'period': 40
		})
		t2 = Task(**{
			'exec_time': 40,
			'deadline': 60,
			'period': 80
		})
		ts = TaskSet()
		ts.append(t1)
		ts.append(t2)

		ms = MultiSegmentTask(**{
			'base_ts': ts,
			'max_option': 4,
			'popt_strategy': 'single'
		})

		self.assertEqual(ms.crit_exec_time, 60)
		self.assertEqual(ms.deadline, 30)
		self.assertEqual(ms.period, 40)

	def test_mst_increment_naive(self):
		t1 = Task(**{
			'exec_time': 20,
			'deadline': 30,
			'period': 40
		})
		t2 = Task(**{
			'exec_time': 40,
			'deadline': 60,
			'period': 80
		})
		ts = TaskSet()
		ts.append(t1)
		ts.append(t2)
		ms = MultiSegmentTask(**{
			'base_ts': ts,
			'max_option': 2,
			'popt_strategy': 'single'
		})
		ms.increment_naive()
		self.assertEqual(ms.popt_list[0], 2)
		ms.increment_naive()
		self.assertEqual(ms.popt_list[1], 2)

	def test_mst_increment_fdsf(self):
		t1 = Task(**{
			'exec_time': 20,
			'deadline': 30,
			'period': 40
		})
		t2 = Task(**{
			'exec_time': 40,
			'deadline': 60,
			'period': 80
		})
		ts = TaskSet()
		ts.append(t1)
		ts.append(t2)
		ms = MultiSegmentTask(**{
			'base_ts': ts,
			'max_option': 2,
			'popt_strategy': 'single'
		})
		ms.increment_fdsf()
		self.assertEqual(ms.popt_list[0], 2)
		self.assertEqual(ms.popt_list[1], 1)
		ms.increment_fdsf()
		self.assertEqual(ms.popt_list[0], 2)
		self.assertEqual(ms.popt_list[1], 2)
		ms.increment_fdsf()
		self.assertEqual(ms.popt_list[0], 2)
		self.assertEqual(ms.popt_list[1], 2)

	def test_mst_increment_cdsf(self):
		t1 = Task(**{
			'exec_time': 20,
			'deadline': 30,
			'period': 40
		})
		t2 = Task(**{
			'exec_time': 40,
			'deadline': 60,
			'period': 80
		})
		ts = TaskSet()
		ts.append(t1)
		ts.append(t2)
		ms = MultiSegmentTask(**{
			'base_ts': ts,
			'max_option': 2,
			'popt_strategy': 'single'
		})
		ms.increment_cdsf()
		self.assertEqual(ms.popt_list[0], 1)
		self.assertEqual(ms.popt_list[1], 2)
		ms.increment_cdsf()
		self.assertEqual(ms.popt_list[0], 2)
		self.assertEqual(ms.popt_list[1], 2)
		ms.increment_cdsf()
		self.assertEqual(ms.popt_list[0], 2)
		self.assertEqual(ms.popt_list[1], 2)

