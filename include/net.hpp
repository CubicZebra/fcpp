// Conan::ImportStart
#pragma once
#include <dlib/dnn.h>
#include <dlib/matrix.h>
// Conan::ImportEnd



using minimal_net = dlib::loss_multiclass_log<
                    dlib::fc<10,
                    dlib::input<dlib::matrix<unsigned char>>
                    >>;



void train_with_random_data();



int predict_random_sample();
