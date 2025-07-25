//! Conan::ImportStart
#pragma once
#include <vector>
//! Conan::ImportEnd


void test_hello();


/**
 * @brief test template func in headers
 * @tparam T vector like
 * @param vec iterable thing of numbers
 * @return a numeric
 * @exporter
 */
template <typename T>
auto test_sum(const std::vector<T>& vec) {
    T sum = T();
    for (const T& elem : vec) { sum += elem; }
    return sum;
}
