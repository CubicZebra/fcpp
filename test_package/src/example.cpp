#include "tst.h"
#include "basic.h"
#include <Eigen/Dense>
#include <vector>
#include <string>
#include <iostream>
#include <generator>


using namespace std;
using namespace Eigen;



// import tst;  // 导入模块
// import <iostream>;
// import <vector>;
// import <string>;
// #include <Eigen/Dense>


std::generator<int> generate_sequence(int start, int end) {
    for (int i = start; i <= end; ++i) {
        co_yield i; // 暂停并返回值
    }
}




int main() {
    tsta();

    std::vector<std::string> vec;
    vec.push_back("test_package");

    tst_print_vector(vec);

    Matrix3d A;
    A << 1, 2, 3,
         4, 5, 6,
         7, 8, 9;

    Vector3d b(1, 2, 3);

    // 2. 打印矩阵和向量
    cout << "矩阵 A:\n" << A << endl;
    cout << "向量 b:\n" << b << endl;

    for (auto v : generate_sequence(3, 15)) { cout << v << endl; };
}
