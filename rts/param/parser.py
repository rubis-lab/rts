import re


def parse_file(fname, target):
    with open(fname) as f:
        # will only read data under [target]
        readData = False
        kwargs = {}
        for line in f:
            if line.startswith('['):
                if readData:
                    return kwargs
                else:
                    m = re.search(r"\[(\w+)\]", line).group(1)
                    if m == target:
                        readData = True
            elif readData:
                if line.strip():
                    word = [x.strip() for x in line.split('=')]
                    kwargs[word[0]] = word[1]
    return kwargs

"""
kv = parse_file('default.cfg', 'sgen')
print(kv.keys())
print(kv.items())
"""
