from my_project.cpp_kernel import int_add

def cpp_add(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return int_add(a, b)