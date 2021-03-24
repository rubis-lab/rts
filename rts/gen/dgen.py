from rts.core.task import Task
from rts.core.ts import TaskSet
from rts.gen.gen import Gen

# from rts.core.dag import DAG

import random
import math

# DAG generator
class Dgen(Gen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_nodes = kwargs.get('min_nodes', 1)
        self.max_nodes = kwargs.get('max_nodes', 10)
        self.edge_prob = kwargs.get('edge_prob', 0.3)
        

        # might not be used
        self.tot_util = kwargs.get('tot_util', 1.0)
        self.utilization_overflow = kwargs.get('util_over', True)
        self.deadline_scale = kwargs.get('deadline_scale', 1.0)
        self.max_mst_util = kwargs.get('max_mst_util', 1.0)
        self.min_seg_size = kwargs.get('min_seg_size', 10)
        self.max_seg_size = kwargs.get('max_seg_size', 20)
        self.max_option = kwargs.get('max_option', 1)
        self.overhead = kwargs.get('overhead', 0.0)
        self.variance = kwargs.get('variance', 0.0)

    def get_leaves(self, e, d):
        leaves = []
        if len(d[e]) == 0:
            return [e]
        else:
            for c in d[e]:
                leaves += self.get_leaves(c, d)
            return leaves

    def bfs(self, d):
        visited = [0]
        q = [0]
        while q:
            s = q.pop(0)
            for c in d[s]:
                if c not in visited:
                    visited.append(c)
                    q.append(c)
        return visited

    def next_dag(self):
        # uniform (implicit deadline)
        period = random.randint(self.min_period, self.min_period)
        deadline = period

        # number of nodes
        n_nodes = random.randint(self.min_nodes, self.max_nodes)

        print('generating {} nodes with p:{} / d:{} '.format(n_nodes, period, deadline))
        print('edge_prob: {}'.format(self.edge_prob))

        # generate edges with probability
        edge_cnt = 0
        edges = {}
        edges_backward = {}
        for n_from in range(1, n_nodes):
            edges[n_from] = []
            edges_backward[n_from] = []

        for n_from in range(1, n_nodes):
            for n_to in range(n_nodes)[n_from + 1:]:
                if random.random() <= self.edge_prob:
                    edge_cnt += 1
                    edges[n_from].append(n_to)
                    edges_backward[n_to].append(n_from)
                    # print('{}->{}'.format(n_from, n_to))
        possible_edges = (n_nodes - 1) * (n_nodes - 2) / 2
        print('edge_cnt: {}, possible_edges: {}, ratio: {}'.format(edge_cnt, possible_edges, edge_cnt / possible_edges))

        # detect starting & ending nodes
        print(edges)
        print(edges_backward)
        end_nodes_list = []
        start_nodes_list = []
        for e in range(1, n_nodes):
            end_nodes_list += self.get_leaves(e, edges)
        for e in range(n_nodes - 1, 0, -1):
            start_nodes_list += self.get_leaves(e, edges_backward)

        end_nodes = set(end_nodes_list)
        print(end_nodes)

        start_nodes = set(start_nodes_list)
        print(start_nodes)

        # make source and sink nodes
        # source: 0
        edges[0] = []
        for n in start_nodes:
            edges[0].append(n)
        # sink: n
        edges[n_nodes] = []
        for n in end_nodes:
            edges[n].append(n_nodes)
        print(edges)
        
        # connect all edges
        topological_sort = self.bfs(edges)
        print(topological_sort)

    def __str__(self):
        info = 'Generator - mstgen\n' + \
            super(type(self), self).__str__() + '\n' + \
            'tot_util = ' + str(self.tot_util) + '\n' + \
            'util_over = ' + str(self.utilization_overflow) + '\n' + \
            'implicit_deadline = ' + str(self.implicit_deadline) + '\n' + \
            'constrained_deadline = ' + str(self.constrained_deadline) + '\n' + \
            'min_seg_size = ' + str(self.min_seg_size) + '\n' + \
            'max_seg_size = ' + str(self.max_seg_size) + '\n' + \
            'max_option = ' + str(self.max_option) + '\n' + \
            'overhead = ' + str(self.overhead) + '\n' + \
            'variance = ' + str(self.variance)

        return info


if __name__ == '__main__':
    gen_param = {
        'min_exec_time': 30,
        'max_exec_time': 100,
        'min_period': 60,
        'max_period': 200,
        'min_deadline': 40,
        'max_deadline': 200,
        'tot_util': 4.0,
        'util_over': True,
        'implicit_deadline': False,
        'constrained_deadline': True,
        'min_seg_size': 10,
        'max_seg_size': 30,
        'max_option': 4
    }
    dg = Dgen(**gen_param)
    dg.next_dag()
