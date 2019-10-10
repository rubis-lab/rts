from rts.core.multiseg import MultiSegment

import unittest


class MultiSegmentTestCase(unittest.TestCase):
	""" Tests for `multiseg.py`."""

	def test_default_multiseg_created(self):
		ms = MultiSegment()
		t = ms.base_pts[0][0].exec_time
		print(t)
		self.assertNotEqual(ms, 1)

