from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.op.stat import Stat
from rts.popt.cho import Cho
from rts.op.rt_app import RTApp

if __name__ == '__main__':
    # create generator
    gen_param = {
        'num_task': 10,
        'min_exec_time': 30,
        'max_exec_time': 100,
        'min_period': 60,
        'max_period': 200,
        'tot_util': 4.0,
        'util_over': False,
    }
    u = Egen(**gen_param)
    print(u)
    print('--------')

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

    #for RTApp Json Output
    rt_app_param = {
        'scale': 100,
        'duration': 20
    }
    rtapp = RTApp(**rt_app_param)

    num_iter = 1
    notify_every = 10000
    for i in range(num_iter):


        if i % notify_every == 0:
            print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))
        # generate tasks
        ts = u.next_task_set()
        if ts == -1:
            print("error")

        # schedulability check param
        sched_param = {
            'num_core': 4.0,
        }

        # single thread
        pts_param_single = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.1,
            'variance': 0.8,
            'popt_strategy': 'single',
        }
        pts = ParaTaskSet(**pts_param_single)
        pts_util = pts.tot_util()
        # additional info for rt app
        with open('additional.info', 'w+') as f:
            f.write(str(pts_util))
        f.close()

            # single thread schedulability
        bcl_naive = BCLNaive(**sched_param)
        sched_single = bcl_naive.is_schedulable(pts)
        stat_single.add(pts_util, sched_single)
        print(pts)
        rtapp.name="single"
        rtapp.create_global()
        print('rtapp name change')
        for t in pts:
            rtapp.add_thr(t)
        print('rtapp name add ts')
        rtapp.to_file()
        print('rtapp file created')
        rtapp.clear_json()


        # max thread
        pts.popt_strategy = 'max'
        pts.serialize_pts()

        # max thread schedulability
        sched_max = bcl_naive.is_schedulable(pts)
        stat_max.add(pts_util, sched_max)
        rtapp.name="max"
        rtapp.create_global()
        print('rtapp name change')
        for t in pts:
            rtapp.add_thr(t)
        print('rtapp name add ts')
        rtapp.to_file()
        print('rtapp file created')
        rtapp.clear_json()

        # random thread
        pts.popt_strategy = 'random'
        pts.serialize_pts()
        rnd_selected_option = pts.popt_list

        # random thread schedulability
        sched_random = bcl_naive.is_schedulable(pts)
        stat_random.add(pts_util, sched_random)
        rtapp.name="random"
        rtapp.create_global()
        print('rtapp name change')
        for t in pts:
            rtapp.add_thr(t)
        print('rtapp name add ts')
        rtapp.to_file()
        print('rtapp file created')
        rtapp.clear_json()

        # cho
        pts.popt_strategy = 'custom'
        pts.serialize_pts()

        # cho schedulability
        popt_param = {
            'num_core': 4.0,
            'max_option': 4,
        }

        cho = Cho(**popt_param)
        pts_cho = cho.is_schedulable(pts)
        sched_cho = True # temporary
        stat_cho.add(pts_util, sched_cho)

        rtapp.name="cho"
        rtapp.create_global()
        print('rtapp name change')
        for t in pts_cho:
            rtapp.add_thr(t)
        print('rtapp name add ts')
        rtapp.to_file()
        print('rtapp file created')
        rtapp.clear_json()

        if not sched_cho:
            if sched_single or sched_max or sched_random:
                print('!!something wrong')
                # print(pts)
            if sched_single:
                print('sched_single')
            if sched_max:
                print('sched_max')
            if sched_random:
                print('sched_random')
                print('rnd dbg:')
                print(rnd_selected_option)
                rnd_dbg = cho.is_schedulable_dbg(pts, rnd_selected_option)
                print(rnd_dbg)
                print('cho verbose result:')
                _, cho_selected_option = cho.is_schedulable_verbose(pts)
                print('cho dbg:')
                print(cho_selected_option)
                cho_dbg = cho.is_schedulable_dbg(pts, cho_selected_option)
                print(rnd_dbg)

    print("single")
    stat_single.print_minimal()
    print("------------")

    print("max")
    stat_max.print_minimal()
    print("------------")

    print("random")
    stat_random.print_minimal()
    print("------------")

    print("cho")
    stat_cho.print_minimal()
    print("------------")
