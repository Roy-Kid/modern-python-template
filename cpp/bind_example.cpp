#include <numeric>
#include <xtensor.hpp>
#include <xtensor/xadapt.hpp>
#include <pybind11/pybind11.h>
#define FORCE_IMPORT_ARRAY
#include <xtensor-python/pyarray.hpp>
#include "example.h"

namespace py = pybind11;

PYBIND11_MODULE(cpp_kernel, m) {

    xt::import_numpy();
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("int_add", &int_add, "A function which adds two numbers",
        py::arg("i"), py::arg("j"));

    m.def("sum_of_sines", 
        &sum_of_sines, "Sum the sines of the input values");

}