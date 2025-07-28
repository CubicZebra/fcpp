//! Conan::ImportStart
#include <iostream>
#include <string>
#include <zlib.h>
#include <Eigen/Dense>
#include <cpptest.hpp>
//! Conan::ImportEnd


/**
 * @brief test function in cpp
 * @exporter
 */
void test_hello() { std::cout << "CPP Compiler is ready!" << std::endl; };


/**
 * @brief test eigen in cpp
 * @exporter
 */
void test_eigen() {
    Eigen::Matrix3d A;
    A << 1, 2, 3,
         4, 5, 6,
         7, 8, 9;
    std::cout << "matrix A:\n" << A << "; Eigen Matrix test done!" << std::endl;
}


/**
 * @brief test Person construction
 * @param n name
 * @param a age
 * @attacher
 */
Person::Person(std::string n, int a) : name(std::move(n)), age(a) {};


/**
 * @brief test Person meth 2
 * @return greet massage
 * @attacher
 */
std::string Person::greet() const { return "Hello, I'm " + name; };


/**
 * @brief zlib requirement test in CPP compiler
 * @exporter
 */
void test_cpp_zlib() {
    const char in[] = "Hello, zlib in CPP!";
    unsigned char out[128] = {0};
    unsigned char rec[128] = {0};
    uLong len_out = sizeof(out);
    uLong len_rec = sizeof(rec);
    int compress_result = compress(out, &len_out, reinterpret_cast<const Bytef*>(in),
        static_cast<uLong>(strlen(in) + 1));
    if (compress_result != Z_OK) {
        std::cerr << "Compression failed with error code: " << compress_result << std::endl;
        return;
    }
    int uncompress_result = uncompress(rec, &len_rec, reinterpret_cast<const Bytef*>(out), len_out);
    if (uncompress_result != Z_OK) {
        std::cerr << "Decompression failed with error code: " << uncompress_result << std::endl;
        return;
    }
    std::cout << "Original: " << in
              << "; Decompressed: " << reinterpret_cast<char*>(rec)
              << "; zlib in C++ test done!" << std::endl;
}