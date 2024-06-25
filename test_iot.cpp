#include <gtest/gtest.h>
#include "iot.h" 
class MeasurementDeviceTest : public ::testing::Test {
protected:
    MeasurementDevice device;

    void SetUp() override {
    }

    void TearDown() override {
    }
};

TEST_F(MeasurementDeviceTest, LogSingle) {
    device.log_single(1, 10.5);
    ASSERT_EQ(device.data.size(), 1);
    EXPECT_EQ(std::get<0>(device.data[0]), 1);
    EXPECT_DOUBLE_EQ(std::get<1>(device.data[0]), 10.5);
}

TEST_F(MeasurementDeviceTest, LogMultiple) {
    std::vector<std::tuple<long, long double>> batch = {
        {1, 10.5},
        {2, 20.5},
        {3, -5.0}
    };
    device.log_multiple(batch);
    ASSERT_EQ(device.data.size(), 3);
    EXPECT_EQ(std::get<0>(device.data[0]), 1);
    EXPECT_DOUBLE_EQ(std::get<1>(device.data[0]), 10.5);
    EXPECT_EQ(std::get<0>(device.data[1]), 2);
    EXPECT_DOUBLE_EQ(std::get<1>(device.data[1]), 20.5);
    EXPECT_EQ(std::get<0>(device.data[2]), 3);
    EXPECT_DOUBLE_EQ(std::get<1>(device.data[2]), -5.0);
}

TEST_F(MeasurementDeviceTest, PeakAccumulation) {
    std::vector<std::tuple<long, long double>> batch = {
        {1, 10.0},
        {2, -5.0},
        {3, 20.0},
        {4, -1.0},
        {5, 3.0}
    };
    device.log_multiple(batch);
    py::tuple result = device.peak_accumulation();
    EXPECT_EQ(py::cast<long>(result[0]), 3);  // Start of peak accumulation
    EXPECT_EQ(py::cast<long>(result[1]), 5);  // End of peak accumulation
    EXPECT_DOUBLE_EQ(py::cast<double>(result[2]), 22.0);  // Highest sum
}

TEST_F(MeasurementDeviceTest, PeakAccumulationEmptyData) {
    py::tuple result = device.peak_accumulation();
    EXPECT_EQ(py::cast<long>(result[0]), -1);
    EXPECT_EQ(py::cast<long>(result[1]), -1);
    EXPECT_DOUBLE_EQ(py::cast<double>(result[2]), -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}