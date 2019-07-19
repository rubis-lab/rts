from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.op.stat import Stat
from rts.popt.cho import Cho
from rts.sched.bar import *
from rts.sched import bcl

if __name__ == '__main__':
	# create generator
	gen_param = {
		'num_task': 10,
		'min_exec_time': 30,
		'max_exec_time': 100,
		'min_period': 60,
		'max_period': 200,
		'tot_util': 4.0,
		'util_over': True,
	}
	u = Egen(**gen_param)
	print(u)

	# logger
	stat_param = {
		'id': 0,
		'min': 0.0,
		'max': 4.0,
		'inc': 0.1,
	}
	stat_single = Stat(**stat_param)
	stat_max = Stat(**stat_param)
	stat_random = Stat(**stat_param)
	stat_cho = Stat(**stat_param)
	n_sched_single = 0
	n_sched_max = 0
	n_sched_random = 0
	n_sched_cho = 0

	stat_single_bcl = Stat(**stat_param)
	stat_single_bar = Stat(**stat_param)
	stat_single_rta = Stat(**stat_param)
	n_sched_single_bcl = 0
	n_sched_single_bar = 0
	n_sched_single_rta = 0

	stat_max_bcl = Stat(**stat_param)
	stat_max_bar = Stat(**stat_param)
	stat_max_rta = Stat(**stat_param)
	n_sched_max_bcl = 0
	n_sched_max_bar = 0
	n_sched_max_rta = 0

	stat_random_bcl = Stat(**stat_param)
	stat_random_bar = Stat(**stat_param)
	stat_random_rta = Stat(**stat_param)
	n_sched_random_bcl = 0
	n_sched_random_bar = 0
	n_sched_random_rta = 0

	notify_every = 1000
	num_iter = 10000
	# count = 0

	for i in range(num_iter):

		if i % notify_every == 0:
			print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))
			
		# generate tasks
		ts = u.next_task_set()
		if ts == -1:
			print("error generating tasks")

		# schedulability check param
		sched_param = {
			'num_core': 4.0,
		}

		# configure pts
		pts_param_single = {
			'base_ts': ts,
			'max_option': 4,
			'overhead': 0.1,
			'variance': 0.7,
			'popt_strategy': 'single',
		}
		pts = ParaTaskSet(**pts_param_single)
		pts_util = pts.tot_util()

		# single thread schedulability
		bcl_naive = BCLNaive(**sched_param)

		# stat_single_bcl.add(pts_util, bcl_naive.is_schedulable(ts))
		sched_single_bcl = bcl_naive.is_schedulable(ts)
		stat_single_bcl.add(pts_util, sched_single_bcl)
		if sched_single_bcl:
			n_sched_single_bcl += 1

		bar = BAR(**sched_param)
		# stat_single_bar.add(pts_util, bar.is_schedulable(ts))
		sched_single_bar = bar.is_schedulable(ts)
		stat_single_bar.add(pts_util, sched_single_bar)
		if sched_single_bar:
			n_sched_single_bar += 1

		# stat_single_rta.add(pts_util, bcl.is_schedulable(ts, **sched_param))
		sched_single_rta = bcl.is_schedulable(ts, **sched_param)
		stat_single_rta.add(pts_util, sched_single_rta)
		if sched_single_rta:
			n_sched_single_rta += 1

		# max thread
		pts.popt_strategy = 'max'
		pts.serialize_pts()

		# max thread schedulability
		# stat_max_bcl.add(pts_util, bcl_naive.is_schedulable(pts))
		sched_max_bcl = bcl_naive.is_schedulable(pts)
		stat_max_bcl.add(pts_util, sched_max_bcl)
		if sched_max_bcl:
			n_sched_max_bcl += 1

		# stat_max_bar.add(pts_util, bar.is_schedulable(pts))
		sched_max_bar = bar.is_schedulable(pts)
		stat_max_bar.add(pts_util, sched_max_bar)
		if sched_max_bar:
			n_sched_max_bar += 1

		# stat_max_rta.add(pts_util, bcl.is_schedulable(pts, **sched_param))
		sched_max_rta = bcl.is_schedulable(pts, **sched_param)
		stat_max_rta.add(pts_util, sched_max_rta)
		if sched_max_rta:
			n_sched_max_rta += 1

		# random thread
		pts.popt_strategy = 'random'
		pts.serialize_pts()
		rnd_selected_option = pts.popt_list

		# random thread schedulability
		# stat_random_bcl.add(pts_util, bcl_naive.is_schedulable(pts))
		sched_random_bcl = bcl_naive.is_schedulable(pts)
		stat_random_bcl.add(pts_util, sched_random_bcl)
		if sched_random_bcl:
			n_sched_random_bcl += 1

		# stat_random_bar.add(pts_util, bar.is_schedulable(pts))
		sched_random_bar = bar.is_schedulable(pts)
		stat_random_bar.add(pts_util, sched_random_bar)
		if sched_random_bar:
			n_sched_random_bar += 1

		# stat_random_rta.add(pts_util, bcl.is_schedulable(pts, **sched_param))
		sched_random_rta = bcl.is_schedulable(pts, **sched_param)
		stat_random_rta.add(pts_util, sched_random_rta)
		if sched_random_rta:
			n_sched_random_rta += 1

		# cho
		pts.popt_strategy = 'custom'
		pts.serialize_pts()

		# cho schedulability
		popt_param = {
			'num_core': 4.0,
			'max_option': 4,
		}

		cho = Cho(**popt_param)
		sched_cho, pts_cho = cho.is_schedulable(pts)
		stat_cho.add(pts_util, sched_cho)
		if sched_cho:
			n_sched_cho += 1

	# print("single")
	# stat_single.print_minimal()
	# print("------------")
	#
	# print("max")
	# stat_max.print_minimal()
	# print("------------")
	#
	# print("random")
	# stat_random.print_minimal()
	# print("------------")
	#
	# print("cho")
	# stat_cho.print_minimal()
	# print("------------")
	print("stat_single_bcl")
	stat_single_bcl.print_minimal()
	print("------------")
	print("stat_single_bar")
	stat_single_bar.print_minimal()
	print("------------")
	print("stat_single_rta")
	stat_single_rta.print_minimal()

	print("------------")
	print("stat_max_bcl")
	stat_max_bcl.print_minimal()
	print("------------")
	print("stat_max_bar")
	stat_max_bar.print_minimal()
	print("------------")
	print("stat_max_rta")
	stat_max_rta.print_minimal()

	print("------------")
	print("stat_random_bcl")
	stat_random_bcl.print_minimal()
	print("------------")
	print("stat_random_bar")
	stat_random_bar.print_minimal()
	print("------------")
	print("stat_random_rta")
	stat_random_rta.print_minimal()

	print("------------")
	print("stat_cho")
	stat_cho.print_minimal()

	print("------------")
	print('total')
	print(num_iter)
	print('n_sched_single')
	print(n_sched_single)
	print('n_sched_max')
	print(n_sched_max)
	print('n_sched_random')
	print(n_sched_random)
	print('n_sched_cho')
	print(n_sched_cho)
	print('n_sched_single_bcl')
	print(n_sched_single_bcl)
	print('n_sched_single_bar')
	print(n_sched_single_bar)
	print('n_sched_single_rta')
	print(n_sched_single_rta)
	print('n_sched_max_bcl')
	print(n_sched_max_bcl)
	print('n_sched_max_bar')
	print(n_sched_max_bar)
	print('n_sched_max_rta')
	print(n_sched_max_rta)
	print('n_sched_random_bcl')
	print(n_sched_random_bcl)
	print('n_sched_random_bar')
	print(n_sched_random_bar)
	print('n_sched_random_rta')
	print(n_sched_random_rta)
