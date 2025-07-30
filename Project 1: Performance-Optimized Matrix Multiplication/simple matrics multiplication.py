import time
import numpy as np


# --- Decorator Function for Timing ---
def time_it(func):
    """
    A decorator that measures the execution time of a function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"\n--- {func.__name__} ---")
        print("Result:")
        if isinstance(result, str):
            print(result)
        elif isinstance(result, np.ndarray):
            print(result)  # NumPy arrays print nicely by default
        else:  # Assuming it's a list of lists for your custom function
            for row in result:
                print(row)
        print(f"Time taken: {elapsed_time:.6f} seconds")
        return result

    return wrapper


@time_it
def matrix_multiply_custom(mat1, mat2):
    """
    Performs matrix multiplication using nested loops.
    Returns the result matrix or an error string if dimensions are incompatible.
    """
    row_mat1 = len(mat1)
    col_mat1 = len(mat1[0])
    row_mat2 = len(mat2)
    col_mat2 = len(mat2[0])

    if col_mat1 != row_mat2:
        return "Error: Number of columns in mat1 must match rows in mat2 for multiplication."

    # Initialize result matrix with correct dimensions (rows of mat1 x columns of mat2)
    matr = [[0 for _ in range(col_mat2)] for _ in range(row_mat1)]

    for i in range(row_mat1):
        for j in range(col_mat2):
            current_sum = 0
            for k in range(col_mat1):  # Iterate through common dimension
                current_sum += mat1[i][k] * mat2[k][j]
            matr[i][j] = current_sum
    return matr


# --- Data Definition ---

import random


def gen_mat(row, col):
    mat = []
    for i in range(row):
        row = []
        for j in range(col):
            row.append(random.randint(10, 20))
        mat.append(row)
    return mat


mat1_list = gen_mat(15, 23)
mat2_list = gen_mat(23, 63)

# --- Custom Matrix Multiplication Execution ---
print("--- Custom Matrix Multiplication ---")
result_custom = matrix_multiply_custom(mat1_list, mat2_list)

# --- NumPy Matrix Operations ---
print("\n--- NumPy Matrix Operations ---")
a_np = np.array(mat1_list)
b_np = np.array(mat2_list)


@time_it
def numpy_dot(a, b):
    return np.dot(a, b)


@time_it
def numpy_matmul(a, b):
    return np.matmul(a, b)


@time_it
def numpy_at_operator(a, b):
    return a @ b


@time_it
def numpy_elementwise_multiply(a, b):
    """
    Performs element-wise multiplication.
    Note: This is NOT matrix multiplication and will raise an error
    if dimensions are incompatible for element-wise operation.
    """
    try:
        return a * b
    except ValueError as e:
        return f"Error: Element-wise multiplication failed - {e}"


@time_it
def numpy_multiply_function(a, b):
    """
    Performs element-wise multiplication using np.multiply().
    Note: This is NOT matrix multiplication.
    """
    try:
        return np.multiply(a, b)
    except ValueError as e:
        return f"Error: np.multiply failed - {e}"


# Execute NumPy operations with the decorator
numpy_dot(a_np, b_np)
numpy_matmul(a_np, b_np)
numpy_at_operator(a_np, b_np)

# These will likely fail or give unexpected results for matrix multiplication context
# because they perform element-wise multiplication and dimensions don't match for that.
# The decorator will catch the error and print it nicely.
print("\n--- Element-wise Multiplications (will likely fail for these dimensions) ---")
numpy_elementwise_multiply(a_np, b_np)
numpy_multiply_function(a_np, b_np)

# This will pass as the dimentions match
mat1_list = gen_mat(5, 6)
mat2_list = gen_mat(5, 6)
a_np = np.array(mat1_list)
b_np = np.array(mat2_list)
numpy_elementwise_multiply(a_np, b_np)
numpy_multiply_function(a_np, b_np)
