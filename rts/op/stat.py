import math


class Stat:
    'Stat class'

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.min = float(kwargs.get('min', 0.0))
        self.max = float(kwargs.get('max', 1.0))
        self.inc = float(kwargs.get('inc', 0.1))
        self.size = int(math.floor((self.max - self.min) / self.inc))
        self.raw_data = [[] for i in range(self.size)]
        self.norm_data = []

    def __str__(self):
        return "%d\t%.2f\t%.2f\t%.2f" % (
            self.id,
            self.min,
            self.max,
            self.inc
        )

    def conv_idx(self, idx):
        return int(math.floor((idx - self.min) / self.inc))

    def add(self, idx, data):
        new_idx = self.conv_idx(idx)
        if new_idx < len(self.raw_data):
            self.raw_data[new_idx].append(data)
        return

    def normalize(self):
        self.norm_data = []
        for dat_idx in self.raw_data:
            num_tot = len(dat_idx)
            num_true = 0

            for dat in dat_idx:
                if dat:
                    num_true += 1

            if num_tot == 0:
                self.norm_data.append(1.0)
            else:
                self.norm_data.append(float(num_true) / float(num_tot))

    def print_short(self):
        self.normalize()
        for i in range(self.size):
            print(str(self.min + i * self.inc) + ", " + str(self.norm_data[i]))

    def print_minimal(self):
        self.normalize()
        for i in range(self.size):
            print(str(self.norm_data[i]))


if __name__ == '__main__':
    stat_param = {
        'id': 0,
        'min': 0.0,
        'max': 2.1,
    }
    s = Stat(**stat_param)
    s.add(0.1, True)
    s.add(0.1, True)
    s.add(0.1, True)
    s.add(0.1, False)
    s.add(0.1, True)
    # s.print_short()
    print(s.conv_idx(0.1))
    print("raw")
    print(s.raw_data)
    s.normalize()
    print("norm")
    print(s.norm_data)
