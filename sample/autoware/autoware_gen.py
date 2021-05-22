# from rts.core.task import Task
# from rts.core.pt import ParaTask
# from rts.core.ts import TaskSet
# from rts.gen.gen import Gen
# from rts.core.dag import DAG
# from rts.core.dagts import DAGTaskSet
# from rts.op.log import new_logger
import os
import yaml
# from tqdm import tqdm
# import numpy as np
# import matplotlib.pyplot as plt
# from rts.op.stat import Stat
# from rts.gen.dgen import Dgen
# from rts.sched.chwa_dag import ChwaDAG
# from rts.popt.cho_dag import ChoDAGTask

import random
import math

#autoware generator
class Customdag(object):
    def __init__(self, **kwargs):
        self.num_node = kwargs.get('num_node', 0)
        self.num_graph = kwargs.get('num_graph', 0)
        self.graph_isolation = kwargs.get('graph_isolation', [])
        self.graphs = kwargs.get('graphs', {})
        self.graph_nodes = self.graphs['nodes']   #lists
        self.graph_edges = self.graphs['edges']   #lists

        self.graph_iter = 0


    def next_graph(self):
                
        nodes_in_graph = self.graph_isolation[graph_iter]
        n_nodes = len(nodes_in_graph)

        # n_id_start = self.graph_isolation[graph_iter][0]
        # n_id_end = self.graph_isolation[graph_iter][-1]

        edge_cnt = 0
        edges = {}
        edges_backward = {}

        for n_from in nodes_in_graph:
            edges[n_from] = []
            edges_backward[n_from] = []
        
        for n_from in nodes_in_graph:
            for n_to in nodes_in_graph:
                
                for e in self.graph_edges:
                    if n_from == e['from'] and n_to == e['to']:
                        edge_cnt += 1
                        edges[n_from].append(n_to)
                        edges_backward[n_to].append(n_from)
        
        end_nodes_list = []
        start_nodes_list = []

        for e in range(1, n_nodes):
            end_nodes_list += self.get_leaves(e, edges)
        for e in range(n_nodes-1, 0, -1):
            start_nodes_list += self.get_leaves(e, edges_backward)
        
        end_nodes = set(end_nodes_list)
        start_nodes = set(start_nodes_list)

        edges[0] = []
        edges_backward[0] = []
        for n in start_nodes:
            edges[0].append(n)
            edges_backward[n].append(0)
        
        edges[n_nodes] = []
        edges_backward[n_nodes] = []
        for n in end_nodes:
            edges[n].append(n_nodes)
            edges_backward[n_nodes].append(n)
        
        nodes_sorted = self.bfs(edges)
        
        graph = {
            'nodes': nodes_sorted,
            'edges': edges,
            'edges_backward': edges_backward,
            'source': 0,
            'sink': n_nodes            
        }

        graph_iter += 1
        return graph

    def generate_template_ptasks(self, g):
        period = g['nodes'][0]

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

        visited = [0]  # start from source vertex (always 0)
        q = [0]
        while q:
            s = q.pop(0)
            # self.log.debug('doing {}'.format(s))
            if in_degree[s] != 0:
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

    def print(self):
        return


if __name__ == '__main__':
    cfg_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'cfg.yaml')
    with open(cfg_file, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    dag = Customdag(**cfg['custom'])
    dag.print()
    exit()