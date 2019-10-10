from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pt import ParaTask
from rts.op import para
from rts.op import tsutil
import random


class ParaTaskSet(object):

    """
    'Parallelizable Task Set'
    Class ParaTask : Generate Parallelizable Taskset\n

    **Import info :** \n
    +----------------+--------------+
    | Package Name   | Module Name  |
    +================+==============+
    | core           | task         |
    +----------------+--------------+
    | core           | ts           |
    +----------------+--------------+
    | core           | pt           |
    +----------------+--------------+
    | op             | para         |
    +----------------+--------------+
    | op             | tsutil       |
    +----------------+--------------+
    """
    cnt = 0

    def __init__(self, **kwargs):
        """
         **Role**: Initialize Parallelizable Taskset\n
         .. note::
          * **max_option** : The maximum parallelize option that \n
          * **overhead** : The increasing rate of **execution_time** on every **parallelization** \n
          * **variance** : How **execution_time**s vary between **thread**s \n
          * **base_ts** : **parallelize task** needs **base_task** ( Default: exec_time=1, deadline=2, period=3 )\n
          * **pt_list** : Save **parallelizable tasks** in a list to make a **parallelizable taskset*\n
          * **populate_pt_list** : See the **"populate_pt_list"**\n
          * **popt_strategy** : parallel option (default **single** )\n
          * **popt_list** : parallel option list for each **pt_list**\n
          * **pts_serialized** :  Generate **taskset** includes **parallelizable tasks** with **parallel option**
          * **serialize_pts** : See the **serialize pts**
         """

        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)
        self.max_opt = kwargs.get('max_option', 1)

        # parallelizer info
        self.overhead = kwargs.get('overhead', 0.0)
        # overhead cap
        # if self.overhead > 0.5:
        #     self.overhead = 3.0
        self.variance = kwargs.get('variance', 0.0)

        # base task set info
        # tmp_ts: fallback task set with a single dummy task.
        tmp_ts = TaskSet()
        tmp_ts.append(Task(**{'exec_time': 1, 'deadline': 2, 'period': 3}))
        self.base_ts = kwargs.get('base_ts', tmp_ts)
        self.pt_list = []

        if kwargs.get('custom', 'False') == 'True':
            self.pt_list = kwargs.get('pt_list', [[]])
        else:
            self.populate_pt_list()

        # pts serialized according to selected option.
        # defaults to single thread for each pt in pts.
        self.popt_strategy = kwargs.get('popt_strategy', 'single')
        self.popt_list = kwargs.get('popt_list', [1 for _ in range(len(self.pt_list))])
        self.pts_serialized = TaskSet()
        self.serialize_pts()
        self.task_list = self.pts_serialized.task_list

        return

    def __del__(self):
        """
        **Role**: Delete Parallelizable Taskset
        .. note:: **cnt** : decreases by 1
        """

        type(self).cnt -= 1

    def __str__(self):
        """
        **Role**: Format for printing Parallelizable Taskset \n

        .. note::
         * **info** = 'id' + 'max_option' + 'base_ts' + 'generated (pts_serialized)'\n
        """
        info = 'id: ' + str(self.id) + '\n' + \
               'max_option: ' + str(self.max_opt) + '\n\n' + \
               'base_ts: ' + '\n' + str(self.base_ts) + '\n' + \
               'generated: \n' + str(self.pts_serialized)

        return info

    def __len__(self):
        """
        **Role**: Returns length of **pts_serialized** \n
        """
        return len(self.pts_serialized)

    def __getitem__(self, idx):
        """
        **Role**: Get **Prallelizable Task** based on index
        """
        return self.pts_serialized[idx]

    def __setitem__(self, idx, thr):
        """
        **Role**: Set **Prallelizable Task**'s parallel option with given value
        """
        self.pts_serialized[idx] = thr
        return

    def __iter__(self):
        """
        **Role**: Set **Prallelizable Task**'s parallel option with given value
        """
        return iter(self.pts_serialized)

    def clear(self):
        """
        **Role**: Delete **Prallelizable Taskset**
        """
        del self.pts_serialized[:]
        del self.pt_list[:]
        return

    def populate_pt_list(self):
        """
        **Role**: Generate **Parallelizabe Task** for given **base_task** with **max_option**, **overhead**, **variance**
        """
        for t in self.base_ts:
            para_task_param = {
                'base_task': t,
                'max_option': self.max_opt,
                'overhead': self.overhead,
                'variance': self.variance,
            }
            pt = ParaTask(**para_task_param)
            self.pt_list.append(pt)
        return

    def serialize_pts(self):
        """
        **Role**: Generate **taskset** includes **parallelizable tasks** with **parallel option**\n

        .. note::
         * :py:const:`if popt_strategy == single` \n
            Generate **Single** parallel option base Parallelizable Taskset\n

         * :py:const:`if popt_strategy == max` \n
            Generate **max** parallel option base Parallelizable Taskset\n

         * :py:const:`if popt_strategy == random` \n
            Generate **random (1 ~ max_option)** parallel option base Parallelizable Taskset\n

         * :py:const:`if popt_strategy == custom` \n
            Generate **value (popt_list argument)** parallel option base Parallelizable Taskset\n

        """
        if self.popt_strategy == 'single':
            self.pts_serialized = para.parallelize_pts_single(self.pt_list)
        elif self.popt_strategy == 'max':
            self.pts_serialized = para.parallelize_pts_max(self.pt_list, **{'max_option': self.max_opt})
        elif self.popt_strategy == 'random':
            del self.popt_list[:]
            for i in range(len(self.base_ts)):
                self.popt_list.append(random.randint(1, self.max_opt))
            # self.pts_serialized = para.parallelize_pts_random(self.pt_list, **{'max_option': self.max_opt})
            self.pts_serialized = para.parallelize_pts_custom(self.pt_list, self.popt_list)
        elif self.popt_strategy == 'custom':
            self.pts_serialized = para.parallelize_pts_custom(self.pt_list, self.popt_list)
        else:
            raise Exception('Parallelization strategy not defined')

    def tot_util(self):
        """
        **Role**: Calculate total utilization (from **"op.tsutil.sum_utilization"**)
        """
        return tsutil.sum_utilization(self.pts_serialized)


if __name__ == '__main__':
    task_param = {
        'exec_time': 4,
        'deadline': 10,
        'period': 10,
    }
    t1 = Task(**task_param)

    task_param = {
        'exec_time': 10,
        'deadline': 20,
        'period': 20,
    }
    t2 = Task(**task_param)

    ts = TaskSet()
    ts.append(t1)
    ts.append(t2)

    pts_param = {
        'base_ts': ts,
        'max_option': 4,
        'overhead': 0.0,
        'variance': 0.3,
        'popt_strategy': 'custom',
        'popt_list': [1, 2],
    }

    pts = ParaTaskSet(**pts_param)

    pts.popt_list = [2, 1]
    pts.serialize_pts()
    print(pts)


