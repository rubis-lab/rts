import math

slack = []


def is_schedulable(pts, **kwargs):
    num_core = float(kwargs.get('num_core', 1.0))

    del slack[:]
    for i in range(len(pts)):
        slack.append(0.0)

    # Terminate condition
    updated = True
    while updated:
        updated = False

        # Check each task's feasibility
        sched = True
        for base_task in pts:
            pass

    return True
