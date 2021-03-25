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
        self.max_nodes = kwargs.get('max_nodes', 20)
        self.edge_prob = kwargs.get('edge_prob', 0.3)

        # might not be used
        # self.tot_util = kwargs.get('tot_util', 1.0)
        # self.utilization_overflow = kwargs.get('util_over', True)
        # self.deadline_scale = kwargs.get('deadline_scale', 1.0)
        # self.max_mst_util = kwargs.get('max_mst_util', 1.0)
        # self.min_seg_size = kwargs.get('min_seg_size', 10)
        # self.max_seg_size = kwargs.get('max_seg_size', 20)
        # self.max_option = kwargs.get('max_option', 1)
        # self.overhead = kwargs.get('overhead', 0.0)
        # self.variance = kwargs.get('variance', 0.0)

    def get_leaves(self, v, edges):
        leaves = []
        if len(edges[v]) == 0:
            return [v]
        else:
            for c in edges[v]:
                leaves += self.get_leaves(c, edges)
            return leaves

    def bfs(self, edges):
        visited = [0]  # start from source vertex (always 0)
        q = [0]
        while q:
            s = q.pop(0)
            for c in edges[s]:
                if c not in visited:
                    visited.append(c)
                    q.append(c)
        return visited

    def next_graph(self):
        # number of nodes
        n_nodes = random.randint(self.min_nodes, self.max_nodes)

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
        print('edge_cnt: {}, possible_edges: {}, ratio: {}'
            .format(edge_cnt, possible_edges, edge_cnt / possible_edges))

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
        edges_backward[0] = []
        for n in start_nodes:
            edges[0].append(n)
            edges_backward[n].append(0)

        # sink: n
        edges[n_nodes] = []
        edges_backward[n_nodes] = []
        for n in end_nodes:
            edges[n].append(n_nodes)
            edges_backward[n_nodes].append(n)
        print(edges)

        # sort nodes
        nodes_sorted = self.bfs(edges)
        print(nodes_sorted)

        graph = {
            'nodes': nodes_sorted,
            'edges': edges,
            'edges_backward': edges_backward,
            'source': 0,
            'sink': n_nodes
        }  # G(V, E)

        return graph

    def next_task(self):
        g = self.next_graph()

        # implicit deadline
        period = random.randint(self.min_period, self.min_period)
        deadline = period

        # dummy node
        t_source = Task(**{
            'exec_time': 0.0,
            'deadline': deadline,
            'period': period,
            'is_dag': True,
            'pred': [],
            'succ': g['edges'][g['source']],
            'is_dummy': True,
        })

        t_sink = Task(**{
            'exec_time': 0.0,
            'deadline': deadline,
            'period': period,
            'is_dag': True,
            'pred': g['edges_backward'][g['sink']],
            'succ': [],
            'is_dummy': True,
        })

        print(t_source)
        print(t_sink)

        # exec time




    def __str__(self):
        info = 'Generator - dgen\n' + \
            super(type(self), self).__str__()

        return info


if __name__ == '__main__':
    gen_param = {
        'min_exec_time': 30,
        'max_exec_time': 100,
        'min_period': 60,
        'max_period': 200,
        'min_deadline': 40,
        'max_deadline': 200,
        'min_nodes': 1,
        'max_nodes': 10,
        'edge_prob': 0.3,
    }
    dg = Dgen(**gen_param)
    dg.next_task()
