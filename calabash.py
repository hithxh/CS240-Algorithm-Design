#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 22:44:15 2018

@author: hexiaohe
"""
import numpy as np
import random
import copy
import time

def read_input():   
    f = open("input/5", "r")
    lines = f.readlines()
    n = int(lines[0])
    edges = []
    for line in lines[1:]:
        u, v, w = line.split()
        edges.append((int(u), int(v), float(w)))
    return n, edges
global n, edges
n, edges = read_input()

def edges_power_matrix():
    epm = np.zeros((2*n+1, 2*n+1), np.float64)
    for u,v,w in edges:
        epm[u+n, v+n] = w
    return epm
global epm
epm = edges_power_matrix()

def power_by_mtt(state, edges):
    state = np.asarray(state)
    m = state.shape[0]
    graph = np.zeros((m+1, m+1), dtype=np.float64)
    
    row = np.zeros(m+1, np.int32)
    row[1:] = state
    row += n
    col = row.reshape(m+1, -1)
    graph = epm[col, row]
    
    mat_l = np.diag(np.sum(graph, axis = 0))
    mat_l -= graph
    det = np.linalg.det(mat_l[1:, 1:])
    return det

def calabash():
    random.seed(0)
    times = 300
    state1, power1 = None, None
    for _ in range(times):
        rand_state = tuple(i * (-1)**random.randrange(1, 3) for i in range(1, n+1))
        random_power = power_by_mtt(rand_state, edges)
        if state1 is None or power1 < random_power:
            state1 = rand_state
            power1 = random_power
    
    state2 = []
    for i in range(1, n+1):
        state_used = copy.copy(state2)
        state_unused = copy.copy(state2)
        state_used.append(i)
        state_unused.append(-i)
        power_used = power_by_mtt(state_used, edges) 
        power_unused = power_by_mtt(state_unused, edges)
        if power_used > power_unused:
            state2.append(i)
        else:
            state2.append(-i)
    power2 = power_by_mtt(state2, edges)
    
    if power1 > power2:
        state = state1
        power = power1
    else:
        state = state2
        power = power2
    print (' '.join('%+d' % i for i in state))
    print ('power:', power)

if __name__ == '__main__':
    time1 = time.time()
    calabash()
    time2 = time.time()
    print('running time:', time2 - time1)