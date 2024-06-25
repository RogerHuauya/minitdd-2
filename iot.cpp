#include <pybind11/pybind11.h>
#include <vector>
#include <tuple>

namespace py = pybind11;

class MeasurementDevice {
public:
    std::vector<std::tuple<long, long double>> data;

    MeasurementDevice() {}

    void log_single(long moment, long double measurement) {
        data.push_back(std::make_tuple(moment, measurement));
    }

    void log_multiple(const std::vector<std::tuple<long, long double>>& batch_measurements) {
        for (const auto& entry : batch_measurements) {
            data.push_back(entry);
        }
    }

    py::tuple peak_accumulation() {
        if (data.empty()) {
            return py::make_tuple(-1, -1, -1);
        }

        double highest_sum = std::numeric_limits<double>::lowest();
        double sum = 0;
        long start_period = 0;
        long end_period = 0;
        long temp_start = 0;

        for (size_t index = 0; index < data.size(); ++index) {
            sum += std::get<1>(data[index]);

            if (sum > highest_sum) {
                highest_sum = sum;
                start_period = temp_start;
                end_period = index;
            }

            if (sum < 0) {
                sum = 0;
                temp_start = index + 1;
            }
        }

        return py::make_tuple(std::get<0>(data[start_period]), std::get<0>(data[end_period]), highest_sum);
    }
};

PYBIND11_MODULE(sensor_module, m) {
    m.doc() = "Measurement Device Interface";

    py::class_<MeasurementDevice>(m, "MeasurementDevice")
        .def(py::init<>())
        .def("log_single", &MeasurementDevice::log_single)
        .def("log_multiple", &MeasurementDevice::log_multiple)
        .def("peak_accumulation", &MeasurementDevice::peak_accumulation)
        .def_readwrite("data", &MeasurementDevice::data);
}