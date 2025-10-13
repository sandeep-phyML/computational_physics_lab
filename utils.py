import os 
import sys
import numpy as np

def Jacobi_iterative(A,b,intial_guess,epsilon):
    n = len(A)
    iter_ = 0.0
    while True:
        new_x = [(1.0/A[i][i])*(b[i] - sum([A[i][j]*intial_guess[j] if i!=j else 0 for j in range(n)])) for i in range(n)]
        distance = np.sqrt(sum([(new_x[i]-intial_guess[i])**2 for i in range(n)]))
        if distance < epsilon:
            print(iter_)
            return new_x
        else :
            intial_guess = new_x
            iter_ += 1.0
        
def Chol_decomp(A):
    n = len(A)
    L = [[0 for _ in range(n)] for _ in range(n)]
    for row_index in range(n):
        for col_index in range(row_index,n):
            if row_index == col_index :
                L[row_index][col_index] = np.sqrt(A[row_index][col_index] - sum([L[row_index][j]**2 for j in range(row_index)]))
            else :
                L[row_index][col_index] = (1/L[row_index][row_index] ) *(A[row_index][col_index] - sum(L[row_index][k]*L[k][col_index] for k in range(row_index)))
                L[col_index][row_index] = L[row_index][col_index]
    return L
def forward_substitution(L,b):
    # inputs are the cholesky decomposed L (L and L* together ) and the b array and returns y 
    n = len(b)
    y = [0 for _ in range(n)]
    for row_index in range(n):
        y[row_index] =( b[row_index] - sum([L[row_index][s_]*y[s_] for s_ in range(0,row_index)]) ) / L[row_index][row_index]
    return y
def backward_substituion(L,y):
    # inputs are the cholesky decomposed L (L and L* together ) and the y array and returns the solution x 
    n = len(y)
    x = [0 for _ in range(n)]
    for row_index in range(n):
        #x_matrix[i] =( y_matrix[i] - sum([LU_matrix[i][s_]*x_matrix[s_] for s_ in range(0,i)]) ) 
        x[-row_index-1] =( y[-row_index-1] - sum([L[-row_index-1][s_]*x[s_] for s_ in range(-row_index,0)]) ) / L[-row_index-1][-row_index-1]
    return x

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
def LU_decompose(A):
    for row_index in range(len(A)):
        for col_index in range(len(A)):
            if row_index == 0:
                pass
                #print("first row" ,A[row_index][col_index])
            else :
                if row_index > col_index :
                    #print(f" L matrix , computation with row index {  row_index} and col index { col_index}")
                    A[row_index][col_index] = (A[row_index][col_index] - sum([A[row_index][s_]*A[s_][col_index] for s_ in range(col_index)]))/A[col_index][col_index]
                    #print(f"Updated matrix element is {A[row_index][col_index]}")
                else:
                    #print(f" U matrix , computation with row index {row_index} and col index {col_index}")
                    A[row_index][col_index] = A[row_index][col_index] - sum([A[row_index][s_]*A[s_][col_index] for s_ in range(row_index)])
                    #print(f"Updated matrix element is {A[row_index][col_index]}")
    return A 

def Midpoint(f,N,a,b,I_true = None):
    h = (b-a)/N
    x_array = []
    fact = 1
    for i in range(N):
        x_element = a + fact* h/2
        x_array.append(x_element)
        fact += 2.0
    I = sum([h*f(item) for item in x_array])
    if I_true:
        print(f"midpoint result for N = {N}:computed value: { I },error : {abs(I_true-I)/I_true * 100}")
        return I , abs(I_true-I)/I_true * 100
    else :
        return I


def Trapezoidal(f,N,a,b,I_true = None):
    h = (b-a)/N
    I = sum([(h/2.0)*(f(a+i*h)+f(a+(i+1)*h)) for i in range(N)])
    if I_true:
        print(f"Trapezoidal result for N = {N}:computed value: { I },error : {abs(I_true-I)/I_true * 100}")
        return I , abs(I_true-I)/I_true * 100
    else :
        return I 
