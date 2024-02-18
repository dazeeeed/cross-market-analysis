import os
import numpy as np

def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_data_path(tree_level=1):
    return os.path.abspath(os.path.join(get_current_path(), tree_level * '../', 'data'))

def running_mean(x, N):
    out = np.zeros_like(x, dtype=np.float64)
    dim_len = x.shape[0]
    for i in range(dim_len):
        if N % 2 == 0:
            a = i - (N-1) // 2
            b = i + (N-1) // 2 + 2
        else:
            a = i - (N-1) // 2
            b = i + (N-1) // 2 + 1

        #cap indices to min and max indices
        a = max(0, a)
        b = min(dim_len, b)
        out[i] = np.mean(x[a:b])
    return out