from my_project.cpp_kernel import int_add, sum_of_sines

def cpp_add(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return int_add(a, b)
    
def cpp_sum_sines(a):
    return sum_of_sines(a)