#include <vector>
#include <iostream>
#include <ctest.h>
#include "cpptest.hpp"
// import "hello.hpp"; // C++23 only


int main() {

    // C test
    test_c_compiler();
    test_c_zlib();
    test_c_pcre();

    // CPP test
    test_hello();
    test_cpp_zlib();
    test_eigen();

    const std::vector<int> nums = {1, 2, 3, 4, 5};
    const auto result = test_sum(nums);
    std::cout << "Sum: " << result << std::endl;

    const Person alice("Alice", 25);
    std::cout << alice.greet() << std::endl;

    const Color<int> red(255, 0, 0);
    red.print();

}
