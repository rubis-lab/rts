from rts.core.task import Task
from rts.core.pt import ParaTask
from rts.core.ts import TaskSet
from rts.gen.gen import Gen
from rts.core.dag import DAG
from rts.core.dagts import DAGTaskSet
from rts.op.log import new_logger

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
        self.max_option = kwargs.get('max_option', 4)
        self.overhead = kwargs.get('overhead', 0.0)
        self.variance = kwargs.get('variance', 0.0)
        self.log = new_logger(__name__)

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
        in_degree = [0 for _ in edges]
        for n_start, n_ends in edges.items():
            for n_end in n_ends:
                in_degree[n_end] += 1
        self.log.debug('in_degree: {}'.format(in_degree))

        visited = [0]  # start from source vertex (always 0)
        q = [0]
        while q:
            s = q.pop(0)
            # self.log.debug('doing {}'.format(s))
            if in_degree[s] != 0:
                self.log.warning('not indegree 0: {}'.format(s))
                self.log.warning('need check')
                q.append(s)
                continue
            else:
                for c in edges[s]:
                    in_degree[c] -= 1
                    if in_degree[c] != 0:
                        continue
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
        self.log.warning('biased_normal failed. check mu/sigma')
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
                    self.log.debug('{}->{}'.format(n_from, n_to))
        possible_edges = (n_nodes - 1) * (n_nodes - 2) / 2
        self.log.debug('edge_cnt: {}, possible_edges: {}, ratio: {}'
            .format(edge_cnt, possible_edges, edge_cnt / possible_edges))

        # detect starting & ending nodes
        self.log.debug('edges: {}'.format(edges))
        self.log.debug('edges_backward: {}'.format(edges_backward))
        end_nodes_list = []
        start_nodes_list = []
        for e in range(1, n_nodes):
            end_nodes_list += self.get_leaves(e, edges)
        for e in range(n_nodes - 1, 0, -1):
            start_nodes_list += self.get_leaves(e, edges_backward)

        end_nodes = set(end_nodes_list)
        self.log.debug('end_nodes: {}'.format(end_nodes))

        start_nodes = set(start_nodes_list)
        self.log.debug('start_nodes: {}'.format(start_nodes))

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
        self.log.debug('edges: {}'.format(edges))
        self.log.debug('edges_backward: {}'.format(edges_backward))

        # sort nodes
        nodes_sorted = self.bfs(edges)
        self.log.debug('nodes_sorted: {}'.format(nodes_sorted))

        graph = {
            'nodes': nodes_sorted,
            'edges': edges,
            'edges_backward': edges_backward,
            'source': 0,
            'sink': n_nodes
        }  # G(V, E)

        return graph

    def generate_template_ptasks(self, g):
        # implicit deadline
        period = random.randint(self.min_period, self.min_period)
        deadline = period
        mu_exec_time = period * self.avg_node_util
        sig_exec_time = mu_exec_time / 2

        # tasks
        ptasks = []
        # source
        t_source = Task(**{
            'exec_time': 0.0,
            'deadline': deadline,
            'period': period,
        })
        pt_source = ParaTask(**{
            'base_task': t_source,
            'max_option': self.max_option,
            'overhead': self.overhead,
            'variance': self.variance,
            'is_dag': True,
            'nid': 0,
            'priority': 0,
            'is_dummy': True,
        })
        ptasks.append(pt_source)

        # general
        for n in g['nodes'][1:len(g['nodes']) - 1]:
            t = Task(**{
                'exec_time': self.biased_normal(mu_exec_time, sig_exec_time),
                'deadline': deadline,
                'period': period,
            })
            pt = ParaTask(**{
                'base_task': t,
                'max_option': self.max_option,
                'overhead': self.overhead,
                'variance': self.variance,
                'is_dag': True,
                'nid': n,
                'priority': n,
            })
            ptasks.append(pt)

        # sink
        t_sink = Task(**{
            'exec_time': 0.0,
            'deadline': deadline,
            'period': period,
        })
        pt_sink = ParaTask(**{
            'base_task': t_sink,
            'max_option': self.max_option,
            'overhead': self.overhead,
            'variance': self.variance,
            'is_dag': True,
            'nid': len(g['nodes']) - 1,
            'priority': len(g['nodes']) - 1,
            'is_dummy': True,
        })
        ptasks.append(pt_sink)

        return ptasks

    def connect_ptasks(self, g, ptasks):
        # forward connection (succ)
        for t_from in ptasks:
            for t_to in g['edges'][t_from.nid]:
                self.log.debug('connecting {}->{}'
                    .format(t_from.nid, t_to))
                task_t_to = next(x for x in ptasks if x.nid == t_to)
                t_from.succ.append(task_t_to)

        # backward connection (pred)
        for t_from in ptasks:
            for t_to in g['edges_backward'][t_from.nid]:
                self.log.debug('connecting(backwards) {}->{}'
                    .format(t_from.nid, t_to))
                task_t_to = next(x for x in ptasks if x.nid == t_to)
                t_from.pred.append(task_t_to)

        return ptasks

    def create_dag(self, ptasks, tid):
        dag = DAG(**{
            'id': tid,
            'tasks': ptasks,
            'deadline': ptasks[0].base_task.deadline,
            'period': ptasks[0].base_task.period,
        })
        return dag

    def next_task(self, tid):
        g = self.next_graph()
        ptasks = self.generate_template_ptasks(g)
        ptasks = self.connect_ptasks(g, ptasks)
        dag = self.create_dag(ptasks, tid)
        return dag

    def next_task_set(self):
        gts = DAGTaskSet()
        for tid in range(self.num_task):
            gt = self.next_task(tid)
            gts.append(gt)
        return gts


if __name__ == '__main__':
    gen_param = {
        'min_period': 60,
        'max_period': 200,
        'min_nodes': 1,
        'max_nodes': 10,
        'edge_prob': 0.3,
        'util_over': True,
        'avg_node_util': 0.2,
        'num_task': 2
    }
    dg = Dgen(**gen_param)
    # dg.next_task()
    dg.next_task_set()
