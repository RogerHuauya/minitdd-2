### README for SmartNet Solutions Sensor API

#### Overview
This project provides an API for managing sensor data for SmartNet Solutions, a company that specializes in IoT sensor networks for smart cities. The system handles registration of sensor readings related to air quality, noise levels, ultraviolet radiation, and traffic flow, and performs efficient data analysis on accumulated readings.

#### Features
- **Sensor Data Registration**: Supports both single-value and multi-value data registration for efficient data handling.
- **Data Analysis**: Identifies periods with the highest accumulated measurements for various environmental factors like air quality, noise, and ultraviolet radiation.

#### API Endpoints
1. **Add Single Measurement**:
   - **Endpoint**: `/add_single/`
   - **Method**: POST
   - **Description**: Registers a single measurement for a specified sensor.
   - **Parameters**:
     - `timestamp`: Integer, timestamp of the measurement.
     - `device_type`: String, type of sensor (e.g., POLLUTION, SUNLIGHT, TRAFFIC_FLOW).
     - `measurement`: Float, measurement value.
   - **Returns**: Confirmation of added measurement with details.

2. **Add Multiple Measurements**:
   - **Endpoint**: `/add_multiple/`
   - **Method**: POST
   - **Description**: Registers multiple measurements for a specified sensor at once.
   - **Parameters**:
     - `device_type`: String, type of sensor.
     - `measurements`: List of dictionaries containing `timestamp` and `measurement`.
   - **Returns**: Confirmation of added measurements with details.

3. **Maximum Accumulated Measurement**:
   - **Endpoint**: `/max_accumulated/`
   - **Method**: GET
   - **Description**: Retrieves the period of time with the highest accumulated measurement for a specified sensor.
   - **Parameters**:
     - `device_type`: String, type of sensor.
   - **Returns**: Details of the period with the highest accumulation or an error message if no data is available.

#### Installation
1. **Requirements**:
   - Python 3.8+
   - FastAPI
   - Uvicorn
   - C++ Compiler supporting C++17
   - Pybind11

2. **Running the API**:
   - Start the API server using the command: `uvicorn main:api --host 127.0.0.1 --port 8000`

#### Development
- **Python-C++ Integration**: Python API utilizes C++ modules for processing sensor data via Pybind11 bindings.
- **Testing**:
  - Python tests are implemented using pytest.
  - C++ functionalities are tested using GTest.
