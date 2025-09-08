#include <gtest/gtest.h>
#include <vector>
#include <cpptest.hpp>



TEST(Title2, Tag1) {
    const std::vector<int> v1 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    const std::vector<int> v2 = {1, 2, 3, 4, 5};

    EXPECT_EQ(test_sum(v1), 55);
    EXPECT_EQ(test_sum(v2), 15);
}


