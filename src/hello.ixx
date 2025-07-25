module;
#include <vector>
export module hello;
import <iostream>;


/**
 * @brief test function in cpp
 */
export void test_hello() { std::cout << "Hello test" << std::endl; }


/**
 * @brief test template func in headers
 * @tparam T vector like
 * @param vec iterable thing of numbers
 * @return a numeric
 */
export template <typename T>
auto test_sum(const std::vector<T>& vec) {
    T sum = T();
    for (const T& elem : vec) { sum += elem; }
    return sum;
}