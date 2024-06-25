import pytest
from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)


# Test Cases for Accumulation Queries
def test_accumulated_valid_with_data():
    sensor = "TRAFFIC"
    ts = int(time.time())
    measurements = [{"timestamp": ts, "read": "100.0"},
                    {"timestamp": ts + 1, "read": "150.0"},
                    {"timestamp": ts + 2, "read": "120.0"},
                    {"timestamp": ts + 3, "read": "200.0"}]

    res_reg = client.post("/add_multiple/", json={"device_type": sensor, "measurements": measurements})
    assert res_reg.status_code == 200

    res_query = client.get(f"/max_accumulated/?device_type={sensor}")
    assert res_query.status_code == 200
    assert "highest_accumulated_value" in res_query.json()
    assert "from" in res_query.json()
    assert "to" in res_query.json()


# Test Cases for Single Registration
def test_single_registration_valid():
    ts = int(time.time())
    sensor = "AIRQUALITY"
    measurement = 10.5
    res = client.post("/add_single/", json={"timestamp": ts, "device_type": sensor, "measurement": measurement})
    assert res.status_code == 200
    assert res.json()["message"] == "Measurement added successfully"
    assert res.json()["device_type"] == sensor
    assert res.json()["timestamp"] == ts
    assert res.json()["measurement"] == measurement


def test_single_registration_invalid_type():
    ts = int(time.time())
    sensor = "NO_SENSOR"
    measurement = 10.5
    res = client.post("/add_single/", json={"timestamp": ts, "device_type": sensor, "measurement": measurement})
    assert res.status_code == 400
    assert "Device type" in res.json()["detail"]


# Test Cases for Multiple Registrations
def test_multiple_registration_valid():
    ts = int(time.time())
    sensor = "ULTRAVIOLETRADIATION"
    measurements = [{"timestamp": ts, "read": "15.7"}, {"timestamp": ts + 1, "read": "16.2"}]
    res = client.post("/add_multiple/", json={"device_type": sensor, "measurements": measurements})
    assert res.status_code == 200
    assert res.json()["message"] == f"{len(measurements)} measurements added successfully"
    assert res.json()["device_type"] == sensor
    assert res.json()["measurements"] == measurements


def test_multiple_registration_invalid_type():
    ts = int(time.time())
    sensor = "NO_SENSOR"
    measurements = [{"timestamp": ts, "read": "15.7"}, {"timestamp": ts + 1, "read": "16.2"}]
    res = client.post("/add_multiple/", json={"device_type": sensor, "measurements": measurements})
    assert res.status_code == 400
    assert "Device type" in res.json()["detail"]


def test_accumulated_no_data():
    sensor = "TRAFFIC"
    res = client.get(f"/max_accumulated/?device_type={sensor}")
    assert res.status_code == 404
    assert "No data available" in res.json()["error"]


def test_accumulated_invalid_type():
    sensor = "NO_SENSOR"
    res = client.get(f"/max_accumulated/?device_type={sensor}")
    assert res.status_code == 400
    assert "Device type" in res.json()["detail"]