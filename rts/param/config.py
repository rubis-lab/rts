import json


def load_config(fname, target):
    with open(fname, "r") as f:
        data = json.load(f)
        print(data)

    if target in data:
        return data[target]

    return {}


if __name__ == '__main__':
    gen_param = load_config("default_config.json", "gen")
    print(gen_param)