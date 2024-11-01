import math
import random


def get_exp_rand_var(l):
    return -(1 / l) * math.log(1 - random.random())
