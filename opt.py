# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 19:19:34 2021

@author: User
"""

import sys
import numpy as np
import crane_simulation

in_file = sys.argv[1]

X = np.loadtxt(in_file)

a, h, b, t, r = X[0], X[1], X[2], X[3], X[4]
o, c1, c2 = crane_simulation.opt_func(a, h, b, t, r)

out_file = in_file[:-5] + 'output'

np.savetxt(out_file, np.array([o, c1, c2]))

