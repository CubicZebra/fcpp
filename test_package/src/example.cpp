#include <Eigen/Dense>
#include <vector>
#include <iostream>
#include <__future.h>
#include <__future.hpp>
#include "hello.hpp"
// import "hello.hpp"; // C++23 only


using namespace std;
using namespace Eigen;


int main() {
    test_hello();

    std::vector<int> nums = {1, 2, 3, 4, 5};
    auto result = test_sum(nums);
    std::cout << "Sum: " << result << std::endl;

    Matrix3d A;
    A << 1, 2, 3,
         4, 5, 6,
         7, 8, 9;

    Vector3d b(1, 2, 3);

    cout << "矩阵 A:\n" << A << endl;
    cout << "向量 b:\n" << b << endl;

    std::cout << "cpp standard: " << CPP_STANDARD << std::endl;
    std::cout << "c standard: " << C_STANDARD << std::endl;
    std::cout << "The value of KK: " << KK << std::endl;

}
