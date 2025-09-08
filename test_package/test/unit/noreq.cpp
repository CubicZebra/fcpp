#include <gtest/gtest.h>



TEST(Title1, Tag1) {
    EXPECT_EQ(1 + 1, 2);
    EXPECT_EQ(4 + 3, 7);
}



TEST(Title1, Tag2) {
    EXPECT_NE(5 + 3, 9);
}
