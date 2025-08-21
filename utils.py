import os 
import sys


def read_matrix(filename):
    with open(filename, 'r') as f:
        matrix = []
        for line in f:
            # Split the line into numbers and convert to int/float
            row = [float(num) for num in line.strip().split()]
            matrix.append(row)
    return matrix

def LCG(n_event,a = 1103515245 , c = 12345 , m = 32768 , normalise = True ):
    event_list = []
    x_i = 15 
    for i in range(n_event):
        y_i = x_i/m
        event_list.append(y_i)
        x_i = (a * x_i + c )% m
    return event_list 