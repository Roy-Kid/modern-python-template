from modern_python_template import cpp_add, cpp_sum_sines

def test_cpp_add():
    assert cpp_add(1, 2) == 3

def test_cpp_sines():
    assert cpp_sum_sines(1) == 0.8414709848078965