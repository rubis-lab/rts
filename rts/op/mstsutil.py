import math


def workload_in_interval_edf(mst, l):
    # body job
    # tasks aligned to deadlines
    w_body_job = [0.0 for _ in range(mst.max_opt)]  # calculated per p

    num_body_job = math.floor(l / mst.period)

    for seg in mst:
        # n_thr = len(seg)  # number of threads in current segment
        for i, thr in enumerate(seg):
            w_body_job[i] += thr.exec_time * num_body_job  # largest thread is the first thread

    # carry-in job
    w_carry_in_job = [0.0 for _ in range(mst.max_opt)]  # calculated per p

    rem_l_carry_in = math.fmod(l, mst.period)  # remaining carry-in length

    for seg in mst[::-1]:  # iterate from last segment
        l_seg_carry_in = min(rem_l_carry_in, seg[0].exec_time)  # seg length defined by the first thread
        for i, thr in enumerate(seg):
            w_carry_in_job[i] += min(thr.exec_time, l_seg_carry_in)

        rem_l_carry_in -= l_seg_carry_in
        if rem_l_carry_in < 0.1:
            break

    w_total = [a + b for a, b in zip(w_body_job, w_carry_in_job)]
    return w_total


def bounded_workload_in_interval_edf(mst, l, bound):
    w_unbounded = workload_in_interval_edf(mst, l)

    w_bounded = 0.0
    for w in w_unbounded:
        w_bounded += min(w, bound)

    return w_bounded
