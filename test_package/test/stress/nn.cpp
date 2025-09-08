#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include <net.hpp>



int sleep(int n) {
    std::this_thread::sleep_for(std::chrono::seconds(n));
    return n + 1;
}



void net_predict() {
    int prediction = predict_random_sample();
}



TEST(Stress, Sleep) {
    EXPECT_EQ(sleep(3), 4);
}



TEST(Stress, Network) {
    EXPECT_NO_THROW(net_predict());
}