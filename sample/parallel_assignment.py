import os
from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.op.stat import Stat
from rts.popt.cho import Cho
from rts.op.rt_app import RTApp
from shutil import copyfile

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

    # for RTApp Json Output
    rt_app_param = {
        'scale': 100,
        'duration': 5,
        'loop': 1000,
    }
    rtapp = RTApp(**rt_app_param)

    notify_every = 100
    num_iter = 100000
    count = 0
    distribute = [0] * 10
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

        # configure pts
        pts_param_single = {
            'base_ts': ts,
            'max_option': 4,
            'overhead': 0.1,
            'variance': 0.8,
            'popt_strategy': 'single',
        }
        pts = ParaTaskSet(**pts_param_single)
        pts_util = pts.tot_util()
        '''
        miss = 0
        if (1.0 < pts_util < 1.2 and distribute[0] < 20):
            miss = 0
        elif (1.2 < pts_util < 1.4 and distribute[1] < 20):
            miss = 0
        elif (1.4 < pts_util < 1.6 and distribute[2] < 20):
            miss = 0
        elif (1.6 < pts_util < 1.8 and distribute[3] < 20):
            miss = 0
        elif (1.8 < pts_util < 2.0 and distribute[4] < 20):
            miss = 0
        elif (2.0 < pts_util < 2.2 and distribute[5] < 20):
            miss = 0
        elif (2.2 < pts_util < 2.4 and distribute[6] < 20):
            miss = 0
        elif (2.4 < pts_util < 2.6 and distribute[7] < 20):
            miss = 0
        elif (2.6 < pts_util < 2.8 and distribute[8] < 20):
            miss = 0
        else:
            miss = 1
        if (miss != 1):
        '''
        # additional info for rt app
        with open('additional.info', 'w+') as f:
            f.write(str(pts_util))
        f.close()

        # single thread schedulability
        bcl_naive = BCLNaive(**sched_param)
        sched_single = bcl_naive.is_schedulable(pts)
        stat_single.add(pts_util, sched_single)

        # create json file for rt-app
        rtapp.name = "single"
        rtapp.create_global()
        for t in pts:
            rtapp.add_thr(t)
        rtapp.to_file()
        rtapp.clear_json()

        if sched_single == False:
            # max thread
            pts.popt_strategy = 'max'
            pts.serialize_pts()

            # max thread schedulability
            sched_max = bcl_naive.is_schedulable(pts)
            stat_max.add(pts_util, sched_max)

            # create json file for rt-app
            rtapp.name = "max"
            rtapp.create_global()
            for t in pts:
                rtapp.add_thr(t)
            rtapp.to_file()
            rtapp.clear_json()

            if sched_max == False:
                # random thread
                pts.popt_strategy = 'random'
                pts.serialize_pts()
                rnd_selected_option = pts.popt_list

                # random thread schedulability
                sched_random = bcl_naive.is_schedulable(pts)
                stat_random.add(pts_util, sched_random)

                # create json file for rt-app
                rtapp.name = "random"
                rtapp.create_global()
                for t in pts:
                    rtapp.add_thr(t)
                rtapp.to_file()
                rtapp.clear_json()

                if sched_random == False:

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

                    # create json file for rt-app
                    rtapp.name = "cho"
                    rtapp.create_global()
                    for t in pts_cho:
                        rtapp.add_thr(t)
                    rtapp.to_file()
                    rtapp.clear_json()

                    if sched_cho == True:
                        '''
                        miss = 0
                        if (1.0 < pts_util < 1.2 and distribute[0] < 20):
                            distribute[0] += 1
                        elif (1.2 < pts_util < 1.4 and distribute[1] < 20):
                            distribute[1] += 1
                        elif (1.4 < pts_util < 1.6 and distribute[2] < 20):
                            distribute[2] += 1
                        elif (1.6 < pts_util < 1.8 and distribute[3] < 20):
                            distribute[3] += 1
                        elif (1.8 < pts_util < 2.0 and distribute[4] < 20):
                            distribute[4] += 1
                        elif (2.0 < pts_util < 2.2 and distribute[5] < 20):
                            distribute[5] += 1
                        elif (2.2 < pts_util < 2.4 and distribute[6] < 20):
                            distribute[6] += 1
                        elif (2.4 < pts_util < 2.6 and distribute[7] < 20):
                            distribute[7] += 1
                        elif (2.6 < pts_util < 2.8 and distribute[8] < 20):
                            distribute[8] += 1
                        else:
                            miss = 1
                        if (miss != 1):
                        '''
                        my_path = os.path.abspath(os.path.dirname(__file__))
                        path = os.path.join(my_path, "../sample/sample_" + str(count) + "/")
                        try:
                            os.mkdir(path)
                        except OSError:
                            print("Creation of the directory %s faild" % path)
                        else:
                            copyfile('single.json', path + 'single.json')
                            copyfile('max.json', path + 'max.json')
                            copyfile('random.json', path + 'random.json')
                            copyfile('cho.json', path + 'cho.json')
                            copyfile('additional.info', path + 'additional.info')
                            count += 1
                        if (count > 100):
                            print("-------------------------------")
                            for arr_iter in distribute:
                                print(arr_iter)
                            break
                    # copy json and add_info to safe place, name it differently
                    # found > 1000 sets --> terminate

                # if not sched_cho:
                #     if sched_single or sched_max or sched_random:
                #         print('!!something wrong')
                #         # print(pts)
                #     if sched_single:
                #         print('sched_single')
                #     if sched_max:
                #         print('sched_max')
                #     if sched_random:
                #         print('sched_random')
                #         print('rnd dbg:')
                #         print(rnd_selected_option)
                #         rnd_dbg = cho.is_schedulable_dbg(pts, rnd_selected_option)
                #         print(rnd_dbg)
                #         print('cho verbose result:')
                #         _, cho_selected_option = cho.is_schedulable_verbose(pts)
                #         print('cho dbg:')
                #         print(cho_selected_option)
                #         cho_dbg = cho.is_schedulable_dbg(pts, cho_selected_option)
                #         print(rnd_dbg)

    # print("single")
    # stat_single.print_minimal()
    # print("------------")

    # print("max")
    # stat_max.print_minimal()
    # print("------------")

    # print("random")
    # stat_random.print_minimal()
    # print("------------")

    # print("cho")
    # stat_cho.print_minimal()
    # print("------------")
