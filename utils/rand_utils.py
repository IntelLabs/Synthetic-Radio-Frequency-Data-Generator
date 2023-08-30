
import numpy as np

def rand_choice(l):
    return np.random.choice(l)

def rand_int(interval):
    if interval[0] == interval[1]:
        return interval[0]
    else:
        return np.random.randint(low=interval[0], high=interval[1]+1)

def rand_float(interval):
    if interval[0] == interval[1]:
        return interval[0]
    else:
        return (interval[1] - interval[0]) * np.random.random_sample() + interval[0]