#include "example.h"

int int_add(int i, int j) {
    return i + j;
}

double sum_of_sines(const xt::xarray<double>& m)
{
    auto sines = xt::sin(m);  // sines does not actually hold values.
    return std::accumulate(sines.begin(), sines.end(), 0.0);
}