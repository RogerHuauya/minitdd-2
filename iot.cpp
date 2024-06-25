#include <pybind11/pybind11.h>
#include "iot.h"

namespace py = pybind11;


PYBIND11_MODULE(sensor_module, m) {
    m.doc() = "Measurement Device Interface";

    py::class_<MeasurementDevice>(m, "MeasurementDevice")
        .def(py::init<>())
        .def("log_single", &MeasurementDevice::log_single)
        .def("log_multiple", &MeasurementDevice::log_multiple)
        .def("peak_accumulation", &MeasurementDevice::peak_accumulation)
        .def_readwrite("data", &MeasurementDevice::data);
}