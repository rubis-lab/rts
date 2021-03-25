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
        self.util_over = kwargs.get('util_over', True)
        self.avg_node_util = kwargs.get('avg_node_util', 0.2)

        # might not be used
        # self.tot_util = kwargs.get('tot_util', 1.0)
        # self.deadline_scale = kwargs.get('deadline_scale', 1.0)
        # self.max_mst_util = kwargs.get('max_mst_util', 1.0)
        # self.min_seg_size = kwargs.get('min_seg_size', 10)
        # self.max_seg_size = kwargs.get('max_seg_size', 20)
        # self.max_option = kwargs.get('max_option', 1)
        # self.overhead = kwargs.get('overhead', 0.0)
        # self.variance = kwargs.get('variance', 0.0)

    def __str__(self):
        info = 'Generator - dgen\n' + \
            super(type(self), self).__str__()

        return info

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

    def biased_normal(self, mu, sigma, cutoff=0.0):
        retries = 5
        for _ in range(retries):
            x = random.gauss(mu, sigma)
            if x > cutoff:
                return x
        print('biased_normal failed. check mu/sigma')
        return cutoff

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

    def generate_template_tasks(self, g):
        # implicit deadline
        period = random.randint(self.min_period, self.min_period)
        deadline = period
        mu_exec_time = period * self.avg_node_util
        sig_exec_time = mu_exec_time / 2

        # tasks
        tasks = []
        # source
        t_source = Task(**{
            'exec_time': 0.0,
            'deadline': deadline,
            'period': period,
            'is_dag': True,
            'is_dummy': True,
        })
        tasks.append(t_source)

        # general
        for n in g['nodes'][1:len(g['nodes']) - 1]:
            t = Task(**{
                'is_dag': True,
                'exec_time': self.biased_normal(mu_exec_time, sig_exec_time),
                'deadline': deadline,
                'period': period,
            })
            tasks.append(t)

        # sink
        t_sink = Task(**{
            'exec_time': 0.0,
            'deadline': deadline,
            'period': period,
            'is_dag': True,
            'is_dummy': True,
        })
        tasks.append(t_sink)

        # print("len: {}".format(len(tasks)))
        # for t in tasks:
        #     print(t)

        return tasks

    def connect_nodes(self, g, tasks):
        for t in tasks:
            print(t)

    def next_task(self):
        g = self.next_graph()
        tasks = self.generate_template_tasks(g)
        self.connect_nodes(g, tasks)


if __name__ == '__main__':
    gen_param = {
        'min_period': 60,
        'max_period': 200,
        'min_nodes': 1,
        'max_nodes': 10,
        'edge_prob': 0.3,
        'util_over': True,
        'avg_node_util': 0.2,
    }
    dg = Dgen(**gen_param)
    dg.next_task()
