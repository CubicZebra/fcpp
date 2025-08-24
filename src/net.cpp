// Conan::ImportStart
#include "net.hpp"
#include <dlib/rand.h>
#include <iostream>
#include <vector>
// Conan::ImportEnd




dlib::matrix<unsigned char> generate_random_image(dlib::rand& rnd) {
    dlib::matrix<unsigned char> img(28, 28);
    for (long r = 0; r < img.nr(); ++r) {
        for (long c = 0; c < img.nc(); ++c) {
            img(r, c) = static_cast<unsigned char>(rnd.get_random_8bit_number());
        }
    }
    return img;
}



void train_with_random_data() {
    dlib::rand rnd;
    std::vector<dlib::matrix<unsigned char>> images;
    std::vector<unsigned long> labels;

    for (int i = 0; i < 1000; ++i) {
        images.push_back(generate_random_image(rnd));  // random images
        labels.push_back(rnd.get_integer_in_range(0, 10)); // random labels
    }

    minimal_net net;
    dlib::dnn_trainer<minimal_net> trainer(net);

    trainer.set_learning_rate(0.01);
    trainer.set_mini_batch_size(32);
    trainer.set_max_num_epochs(2);

    trainer.train(images, labels);

    dlib::serialize("random_model.dat") << net;
    std::cout << "training done，model has been saved as random_model.dat" << std::endl;
}



int predict_random_sample() {
    minimal_net net;
    dlib::deserialize("random_model.dat") >> net;

    dlib::rand rnd;
    dlib::matrix<unsigned char> test_img = generate_random_image(rnd);

    return net(test_img);
}