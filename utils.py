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

def sim_1_third(f,a,b,N):
    h = (b-a)/N
    int_sum = 0.0
    x = a
    for i in range(N+1):
        if i == 0 or i == N :
            int_sum += f(x)
        elif i % 2 == 0 :
            int_sum += 2.0 * f(x)
        elif i % 2 == 1 :
            int_sum += 4.0 * f(x)
        x += h
    return h/3.0 * int_sum

def Gaussian_Quad(f,a,b,roots,weights):
    result = 0.0
    for i in range(len(roots)):
        result += f(roots[i],a,b) * weights[i]
    result = result * (b-a)/2
    return result

def find_int_Gaussian_Quad(f,a,b,f_true,Gaussian_Quad,epsilon=1e-8, n_max = 30):
    for i in range(n_max):
        roots , weights = np.polynomial.legendre.leggauss(i+1)
        result = Gaussian_Quad(f,a,b,roots,weights)
        if abs(result-f_true) <= epsilon :
            print(f"The estimated value is : {result}, for n : {i+1}")
            break 

def Forward(a,b,h,f,y_a):
    y_s = [y_a]
    x_s = [a]
    while True:
        y_s.append(y_s[-1] + h * f(y_s[-1],x_s[-1]) )
        x_s.append(x_s[-1]+h)
        if x_s[-1] >= b:
            break
    return x_s ,y_s
def Predictor_corrector(a,b,h,f,y_a):
    y_s = [y_a]
    x_s = [a]
    while True:
        k1 = h * f(y_s[-1],x_s[-1])
        k2 = h * f(y_s[-1]+k1,x_s[-1]+h)
        y_s.append(y_s[-1] + (k1+k2)/2.0 )
        x_s.append(x_s[-1]+h)
        if x_s[-1] >= b:
            break
    return x_s ,y_s

# -------------------- Assignment - 16 --------------------------- 

def LagrangeInterpolation(x_list,y_list,x_in):
    n = len(x_list)
    y_pred = 0
    for i in range(n):
        prod_k = 1.0
        for k in range(n):
            if i != k :
                prod_k *=  (x_in-x_list[k])/(x_list[i]-x_list[k])
        y_pred += y_list[i] * prod_k
    return y_pred

def LinearSquareFit(x_list,y_list,sigma_i = None):
    " y = a1 + a2x"
    a = 0.0
    b =  0.0
    n = len(x_list)
    if sigma_i == None:
        sigma_i = []
        for i in range(n):
            sigma_i.append(1.0)
    S = sum([1.0/sigma_i[i]**2 for i in range(n)])
    S_xx = sum([x_list[i]**2/sigma_i[i]**2 for i in range(n)])
    S_yy = sum([y_list[i]**2/sigma_i[i]**2 for i in range(n)])
    S_x = sum([x_list[i]/sigma_i[i]**2 for i in range(n)])
    S_y = sum([y_list[i]/sigma_i[i]**2 for i in range(n)])
    S_xy = sum([x_list[i]*y_list[i]/sigma_i[i]**2 for i in range(n)])
    Delta = S*S_xx - S_x**2
    a1 = (S_xx*S_y-S_x*S_xy)/Delta 
    a2 = (S_xy*S-S_x*S_y)/Delta
    r_square =S_xy**2 / ( S_xx * S_yy )
    return a1, a2 ,  r_square

