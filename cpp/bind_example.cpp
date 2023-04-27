#include <pybind11/pybind11.h>
#include "example.h"

namespace py = pybind11;

PYBIND11_MODULE(cpp_kernel, m) {

        m.doc() = "pybind11 example plugin"; // optional module docstring

        m.def("int_add", &int_add, "A function which adds two numbers",
            py::arg("i"), py::arg("j"));

}