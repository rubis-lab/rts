import json
from rts.core.task import Task


class RTApp(object):
    def __init__(self, **kwargs):
        self.json_data = {}
        self.exp_duration = kwargs.get('duration', 10)
        self.name = kwargs.get('name', 'exp')
        self.scale = kwargs.get('scale', 1000)
        self.comp = kwargs.get('comp', 1.1)
        self.create_global()
        self.thr_cnt = 0

    def create_global(self):
        self.json_data['global'] = {
            'duration': self.exp_duration,
            'default_policy': 'SCHED_DEADLINE',
            'log_basename': self.name,
            'ftrace': True,
            'gnuplot': True
        }
        self.json_data['tasks'] = {}

    def add_thr(self, t):
        thr_name = 'thread' + str(self.thr_cnt)
        tasks = self.json_data['tasks']
        tasks[thr_name] = {
            'runtime': int(self.scale * t.exec_time),
            'dl-runtime': int(self.scale * t.exec_time * self.comp),
            'dl-deadline': int(self.scale * t.deadline),
            'dl-period': int(self.scale * t.period),
            'timer': {
                'ref': 'unique' + str(self.thr_cnt),
                'period': int(self.scale * t.period * self.comp),
		'mode': 'absolute'
            }
        }
        self.thr_cnt += 1

    def clear_json(self):
        self.thr_cnt = 0
        self.json_data = {}

    def to_file(self):
        with open(self.name + '.json', 'w') as outfile:
            json.dump(self.json_data, outfile, indent=4, sort_keys=True)


if __name__ == '__main__':
    rt_app_param = {
        'name': 'exp01',
        'scale': 100,
        'duration': 20
    }
    rtapp = RTApp(**rt_app_param)
    t = Task(**{'exec_time': 1, 'deadline': 2, 'period': 3})
    rtapp.add_thr(t)
    t = Task(**{'exec_time': 2, 'deadline': 3, 'period': 4})
    rtapp.add_thr(t)
    rtapp.to_file()
