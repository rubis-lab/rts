from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.core.pt import ParaTask
from rts.op import para
from rts.op import tsutil
import random
import operator
from math import isclose, floor
from rts.op.log import new_logger


class DAG(object):
    """
    'DAG Task'
    """
    cnt = 0

    def __init__(self, **kwargs):
        type(self).cnt += 1
        self.id = kwargs.get('id', type(self).cnt)
        self.log = new_logger(__name__)

        # he2019
        self.lall = {}
        self.in_degree = {}
        self.tasks = kwargs.get('tasks')  # topological
        self.sort_tasks()
        self.assign_priority_he2019()
        self.longest_chain = self.detect_longest_chain()
        self.graph_len()
        self.graph_vol()

        # gedf
        self.deadline = kwargs.get('deadline')
        self.period = kwargs.get('period')
        self.carry_in_calculated = False

        w_100 = self.workload_gedf(100)
        self.log.info('w_100: {}'.format(w_100))

        w_200 = self.workload_gedf(200)
        self.log.info('w_200: {}'.format(w_200))

        w_300 = self.workload_gedf(300)
        self.log.info('w_300: {}'.format(w_300))

        w_400 = self.workload_gedf(400)
        self.log.info('w_400: {}'.format(w_400))

        # parallelize

    def sort_tasks(self):
        self.tasks.sort(key=operator.attrgetter('priority'))
        return

    def calc_len_he2019(self):
        # lf
        lf = {}
        t_source = self.tasks[0]
        lf[t_source] = t_source.exec_time
        for t in self.tasks:
            lf[t] = t.exec_time
            if len(t.pred) != 0:
                lf[t] += max(list(map(lambda x: lf[x], t.pred)))

        # lb
        lb = {}
        t_sink = self.tasks[-1]
        lb[t_sink] = t_sink.exec_time

        for t in self.tasks[::-1]:
            lb[t] = t.exec_time
            if len(t.succ) != 0:
                lb[t] += max(list(map(lambda x: lb[x], t.succ)))

        # l
        lall = {}
        for t in self.tasks:
            lall[t] = lf[t] + lb[t] - t.exec_time

        for t in self.tasks:
            self.log.debug(
                't.nid: {}, t.exec_time: {}, lf: {}, lb: {}, lall: {}'
                .format(t.nid, t.exec_time, lf[t], lb[t], lall[t]))

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
        self.log.debug('longest_chain: {}'.format(longest_chain))
        for t in longest_chain:
            self.log.debug(t.nid)
        return longest_chain

    def graph_len(self, recalculate=True):
        if recalculate:
            longest_chain = self.detect_longest_chain()
        else:
            longest_chain = self.longest_chain
        graph_len = 0
        for t in longest_chain:
            graph_len += t.exec_time
        self.log.debug('graph_len: {}'.format(graph_len))
        return graph_len

    def graph_vol(self):
        graph_vol = 0
        for t in self.tasks:
            graph_vol += t.exec_time
        self.log.debug('graph_vol: {}'.format(graph_vol))
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

            self.log.debug('dangling_nodes: {}'
                .format(list(map(lambda x: x.nid, dangling_nodes))))
            # find arg max lall node
            max_lall = max(list(map(lambda x: self.lall[x], dangling_nodes)))

            # perform argmax (ties broken by topological order)
            for d in dangling_nodes:
                if isclose(self.lall[d], max_lall):
                    max_node = d
                    break

            self.log.debug('max_node: {}'.format(max_node.nid))
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
                    break

            self.log.debug('max_node_s: {}'.format(max_node_s.nid))

            # create sub_g
            max_node_s_ancestors = self.get_all_ance_sorted(max_node_s)
            self.log.debug('max_node_s_ancestors: {}'
                .format(list(map(lambda x: x.nid, max_node_s_ancestors))))
            self.log.debug('not_visited: {}'
                .format(list(map(lambda x: x.nid, not_visited))))
            new_sub_g = []
            if len(max_node_s_ancestors) != 0:
                for n in not_visited:
                    if n in max_node_s_ancestors:
                        new_sub_g.append(n)

            # recurse
            if len(new_sub_g) != 0:
                self.log.debug('recurse with new_sub_g: {}'
                    .format(list(map(lambda x: x.nid, new_sub_g))))
                new_visited, prio = self.assign_priority_inner(new_sub_g, prio)
                visited += new_visited
                for n in new_visited:
                    not_visited.remove(n)

        return visited, prio

    def assign_priority_he2019(self):
        self.lall = self.calc_len_he2019()
        self.log.debug('lall: {}'.format(self.lall))
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
        self.log.debug('not_visited: {}'.format(not_visited))
        prio = 1

        v, prio = self.assign_priority_inner(not_visited, prio)
        visited += v

        for idx, t in enumerate(visited):
            self.log.debug('prio: {} / nid: {} / lall: {}'
                .format(t.priority, t.nid, self.lall[t]))
        return visited

    def prepare_carry_in_calculation(self):
        self.sort_tasks()
        for t in self.tasks:
            t.start_time = self.deadline
            t.finish_time = self.deadline
        # for t in self.tasks:
        #     if len(t.pred) == 0:
        #         continue
        #     for p in t.pred:
        #         if p.start_time < t.finish_time:
        #             t.finish_time = p.start_time
        #     t.start_time = t.finish_time - t.exec_time
        for t in self.tasks[::-1]:
            if len(t.succ) == 0:
                continue
            for p in t.succ:
                if p.start_time < t.finish_time:
                    t.finish_time = p.start_time
            t.start_time = t.finish_time - t.exec_time
        for t in self.tasks:
            self.log.debug('{}({}): s[{}] e[{}] f[{}]'
                .format(t.priority, t.nid,
                    t.start_time, t.exec_time, t.finish_time))

    def carry_in_gedf(self, _l=0):
        # assumes maximal parallelization AND maximal possible cores
        # determine which tasks to be included
        # start from lowest priority(backmost)
        if not self.carry_in_calculated:
            self.prepare_carry_in_calculation()
            self.carry_in_calculated = True

        w_carry_in = 0.0
        cutoff = self.deadline - _l
        for t in self.tasks:
            #           cutoff (D - l)
            # case 1)      |
            #              |    <--- t --->
            if t.start_time > cutoff:
                w_carry_in += t.exec_time
            # case 2)      |
            #  <--- t ---> |
            elif t.finish_time < cutoff:
                w_carry_in += 0.0
            # case 3)      |
            #          <--- t --->
            else:
                w_carry_in += t.finish_time - cutoff

        return w_carry_in

    def workload_gedf(self, _l):
        n_whole_inclusion = floor(_l / self.period)
        w_body = n_whole_inclusion * self.graph_vol()

        remaining_l = _l - n_whole_inclusion * self.period
        w_carry_in = self.carry_in_gedf(remaining_l)

        return w_body + w_carry_in

    def configure_custom(self, options):
        for t, opt in zip(self.tasks, options):
            t.configure_pt(opt)
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
        return len(self.tasks)  # number of segments

    def __getitem__(self, idx):
        return self.tasks[idx]  # get segment

    def __setitem__(self, idx, t):
        self.tasks[idx] = t  # set segment
        return

    def __iter__(self):
        return iter(self.tasks)
