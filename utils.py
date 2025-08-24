import os 
import sys


def read_matrix(filename):
    with open(filename, 'r') as f:
        matrix = []
        for line in f:
            # Split the line into numbers and convert to int/float
            row = [float(num) for num in line.strip().split()]
            if len(row) == 1 :
                row = row[0]
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
def gauss_jordan(A, B):
    n = len(A)
    # Create augmented matrix
    aug_matrix = [A[i] + [B[i]] for i in range(n)]
    for i in range(n):
        # Partial pivoting
        max_row = max(range(i, n), key=lambda r: abs(aug_matrix[r][i]))
        if aug_matrix[max_row][i] == 0:
            raise ValueError("Matrix is singular and cannot be solved.")
        aug_matrix[i], aug_matrix[max_row] = aug_matrix[max_row], aug_matrix[i]
        # Normalize pivot row
        pivot = aug_matrix[i][i]
        aug_matrix[i] = [x / pivot for x in aug_matrix[i]]
        # Eliminate all other rows
        for j in range(n):
            if j != i:
                factor = aug_matrix[j][i]
                aug_matrix[j] = [
                    aug_matrix[j][k] - factor * aug_matrix[i][k]
                    for k in range(n + 1)
                ]
    # return ,  X 
    return [row[-1] for row in aug_matrix]

