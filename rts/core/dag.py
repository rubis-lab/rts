from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pt import ParaTask
from rts.op import para
from rts.op import tsutil
import random
import operator
from math import isclose


class DAG(object):
    """
    'DAG Task'
    """
    cnt = 0

    def __init__(self, **kwargs):
        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)

        # he2019
        self.lall = {}
        self.in_degree = {}
        self.tasks = kwargs.get('tasks')  # topological
        self.sort_tasks()
        self.assign_priority_he2019()
        self.longest_chain = self.detect_longest_chain()
        self.graph_len()
        self.graph_vol()

    def sort_tasks(self):
        self.tasks.sort(key=operator.attrgetter('priority'))
        return

    def calc_len_he2019(self):
        # lf
        lf = {}
        t_source = self.tasks[0]
        lf[t_source] = t_source.exec_time
        for t in self.tasks:
            # print(t)
            lf[t] = t.exec_time
            if len(t.pred) != 0:
                lf[t] += max(list(map(lambda x: lf[x], t.pred)))

        # lb
        lb = {}
        t_sink = self.tasks[-1]
        lb[t_sink] = t_sink.exec_time

        for t in self.tasks[::-1]:
            # print(t)
            lb[t] = t.exec_time
            if len(t.succ) != 0:
                lb[t] += max(list(map(lambda x: lb[x], t.succ)))

        # l
        lall = {}
        for t in self.tasks:
            lall[t] = lf[t] + lb[t] - t.exec_time

        # for t in self.tasks:
        #     print('t.nid: {}, t.exec_time: {}, lf: {}, lb: {}, lall: {}'
        #         .format(t.nid, t.exec_time, lf[t], lb[t], lall[t]))

        return lall

    def detect_longest_chain(self):
        # # identify all max nodes
        # max_lall = max(self.lall)
        # max_nodes = []
        # for t in self.tasks:
        #     if isclose(self.lall[t], max_lall):
        #         max_nodes.append(t)

        # find longest chain
        longest_chain = []
        t_source = self.tasks[0]
        longest_chain.append(t_source)

        # recursively
        t = t_source
        while len(t.succ) != 0:
            max_lall = max(list(map(lambda x: self.lall[x], t.succ)))
            for c in t.succ:
                if isclose(self.lall[c], max_lall):
                    longest_chain.append(c)
                    t = c
                    break
        # print('longest_chain: {}'.format(longest_chain))
        # for t in longest_chain:
        #     print(t.nid)
        return longest_chain

    def graph_len(self, recalculate=True):
        if recalculate:
            longest_chain = self.detect_longest_chain()
        else:
            longest_chain = self.longest_chain
        graph_len = 0
        for t in longest_chain:
            graph_len += t.exec_time
        print('graph_len: {}'.format(graph_len))
        return graph_len

    def graph_vol(self):
        graph_vol = 0
        for t in self.tasks:
            graph_vol += t.exec_time
        print('graph_vol: {}'.format(graph_vol))
        return graph_vol

    def get_all_ance(self, node):
        # get all ancestors
        ance = []
        for c in node.pred:
            ance.append(c)
            if len(c.pred) != 0:
                ance += self.get_all_ance(c)
        return ance

    def get_all_ance_sorted(self, node):  # sorted by nid
        ancestors = list(set(self.get_all_ance(node)))  # unsorted
        ancestors.sort(key=operator.attrgetter('nid'))
        return ancestors

    def assign_priority_inner(self, sub_g, prio):
        visited = []
        not_visited = sub_g
        while not_visited:
            # check dangling nodes
            dangling_nodes = []
            for n in not_visited:
                if self.in_degree[n] == 0:
                    dangling_nodes.append(n)

            print('dangling_nodes: {}'
                .format(list(map(lambda x: x.nid, dangling_nodes))))
            # find arg max lall node
            max_lall = max(list(map(lambda x: self.lall[x], dangling_nodes)))

            # perform argmax (ties broken by topological order)
            for d in dangling_nodes:
                if isclose(self.lall[d], max_lall):
                    max_node = d

            print('max_node: {}'.format(max_node.nid))
            # assign priority
            max_node.priority = prio
            prio += 1

            # update tracking info
            visited.append(max_node)
            not_visited.remove(max_node)
            for s in max_node.succ:
                self.in_degree[s] -= 1

            # continue with other dangling vertex when there is no sucessor
            if len(max_node.succ) == 0:
                continue

            # again, find maximum node among them
            max_lall_s = max(list(map(lambda x: self.lall[x], max_node.succ)))
            for s in max_node.succ:
                if isclose(self.lall[s], max_lall_s):
                    max_node_s = s

            print('max_node_s: {}'.format(max_node_s.nid))

            # create sub_g
            max_node_s_ancestors = self.get_all_ance_sorted(max_node_s)
            print('max_node_s_ancestors: {}'
                .format(list(map(lambda x: x.nid, max_node_s_ancestors))))
            print('not_visited: {}'
                .format(list(map(lambda x: x.nid, not_visited))))
            new_sub_g = []
            if len(max_node_s_ancestors) != 0:
                for n in not_visited:
                    if n in max_node_s_ancestors:
                        new_sub_g.append(n)

            # recurse
            if len(new_sub_g) != 0:
                print('recurse with new_sub_g: {}'
                    .format(list(map(lambda x: x.nid, new_sub_g))))
                new_visited = self.assign_priority_inner(new_sub_g, prio)
                visited += new_visited
                for n in new_visited:
                    not_visited.remove(n)

        return visited

    def assign_priority_he2019(self):
        self.lall = self.calc_len_he2019()
        print('lall: {}'.format(self.lall))
        self.in_degree = {}
        for t in self.tasks:
            self.in_degree[t] = len(t.pred)

        # track visited / not_visited nodes
        not_visited = []
        for t in self.tasks:
            not_visited.append(t)

        # start with source node
        t_source = self.tasks[0]
        visited = [t_source]
        not_visited.remove(t_source)
        for s in t_source.succ:
            self.in_degree[s] -= 1
        print('not_visited: {}'.format(not_visited))
        prio = 1

        visited += self.assign_priority_inner(not_visited, prio)

        for idx, t in enumerate(visited):
            print('prio: {} / nid: {} / lall: {}'
                .format(t.priority, t.nid, self.lall[t]))
        return

    def __del__(self):
        type(self).cnt -= 1

    def __str__(self):
        info = 'id: ' + str(self.id) + '\n' + \
            'max_option: ' + str(self.max_opt) + '\n' + \
            'popt_strategy: ' + self.popt_strategy + '\n' + \
            'num_segments: ' + str(len(self)) + '\n' + \
            'tot_util: ' + str(self.tot_util()) + '\n\n' + \
            'generated: \n'
        for i, ts in enumerate(self.ts_list):
            info += 'segment ' + str(i + 1) + '\n' + \
                str(ts) + '\n'
        return info

    def __len__(self):
        return len(self.ts_list)  # number of segments

    def __getitem__(self, idx):
        return self.ts_list[idx]  # get segment

    def __setitem__(self, idx, ts):
        self.ts_list[idx] = ts  # set segment
        return

    def __iter__(self):
        return iter(self.ts_list)

    def clear(self):
        del self.ts_list[:]
        del self.pt_list[:]
        return

    def populate_pt_list(self):
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

    def increment_naive(self):
        new_popt_list = []
        for opt in self.popt_list:
            if opt < self.max_opt:
                new_popt_list.append(opt + 1)
            else:  # won't increment over max_opt
                new_popt_list.append(opt)
        self.popt_list = new_popt_list
        self.popt_strategy = 'custom'
        self.update_ts_list()
        return

    def increment_fdsf(self):
        # farther from deadline segment first
        # or... first segment first
        new_popt_list = []
        incremented = False
        for opt in self.popt_list:
            if not incremented:
                if opt < self.max_opt:
                    new_popt_list.append(opt + 1)
                    incremented = True  # increment only a single option
                else:  # won't increment over max_opt
                    new_popt_list.append(opt)
            else:
                new_popt_list.append(opt)
        self.popt_list = new_popt_list
        self.popt_strategy = 'custom'
        self.update_ts_list()
        return

    def increment_cdsf(self):
        # closer to deadline segment first
        # or... last segment first
        new_popt_list = []
        incremented = False
        for opt in self.popt_list[::-1]:
            if not incremented:
                if opt < self.max_opt:
                    new_popt_list.append(opt + 1)
                    incremented = True  # increment only a single option
                else:  # won't increment over max_opt
                    new_popt_list.append(opt)
            else:
                new_popt_list.append(opt)
        self.popt_list = new_popt_list[::-1]  # reverse it back
        self.popt_strategy = 'custom'
        self.update_ts_list()
        return

    def update_ts_list(self):
        if self.popt_strategy == 'single':
            self.popt_list = [1 for _ in range(len(self))]
            self.ts_list = para.parallelize_multiseg_single(self.pt_list)
        elif self.popt_strategy == 'max':
            self.popt_list = [self.max_opt for _ in range(len(self))]
            self.ts_list = para.parallelize_multiseg_max(self.pt_list, **{'max_option': self.max_opt})
        elif self.popt_strategy == 'random':  # deprecated
            del self.popt_list[:]
            for i in range(len(self.base_ts)):
                self.popt_list.append(random.randint(1, self.max_opt))
            self.ts_list = para.parallelize_multiseg_custom(self.pt_list, self.popt_list)
        elif self.popt_strategy == 'custom':
            self.ts_list = para.parallelize_multiseg_custom(self.pt_list, self.popt_list)
        else:
            raise Exception('Parallelization strategy not defined')

        # update longest exec_time
        self.update_exec_time()
        return

    def update_exec_time(self):
        c_e = 0.0
        e = 0.0
        # print('used_option')
        # print(self.popt_list)
        for ts in self.ts_list:
            c_e += ts[0].exec_time  # sum of largest exec_time (longest path)
            # print('ts[0].exec_time')
            # print(ts[0].exec_time)
            for t in ts:
                e += t.exec_time  # sum of all exec_time
                # print('t.exec_time')
                # print(t.exec_time)

        self.crit_exec_time = c_e
        self.exec_time = e
        # print('exec_time_updated')
        # print('c_e')
        # print(c_e)
        # print('e')
        # print(e)
        return

    def tot_util(self):
        return self.exec_time / self.period
#
#
# if __name__ == '__main__':
#     t1 = Task(**{
#         'exec_time': 20,
#         'deadline': 30,
#         'period': 40
#     })
#     t2 = Task(**{
#         'exec_time': 40,
#         'deadline': 60,
#         'period': 80
#     })
#     ts = TaskSet()
#     ts.append(t1)
#     ts.append(t2)
#
#     ms = MultiSegmentTask(**{
#         'base_ts': ts,
#         'max_option': 4,
#         'popt_strategy': 'max'
#     })
#
#     print(ms)
#     print(ms.crit_exec_time)
#     print(ms.exec_time)
#     print(ms.tot_util())
