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

