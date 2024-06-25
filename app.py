import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List, Dict
import iot as monitoring

api = FastAPI()

pollution_monitor = monitoring.MeasurementDevice()
sunlight_monitor = monitoring.MeasurementDevice()
vehicle_flow_monitor = monitoring.MeasurementDevice()

devices = {
    "POLLUTION": pollution_monitor,
    "SUNLIGHT": sunlight_monitor,
    "TRAFFIC_FLOW": vehicle_flow_monitor
}


@api.post("/add_single/")
async def add_single(timestamp: int, device_type: str, measurement: float):
    if device_type not in devices:
        raise HTTPException(status_code=400, detail=f"Device type '{device_type}' not supported.")
    
    devices[device_type].log_single(timestamp, measurement)
    
    return {
        "message": "Measurement added successfully",
        "device_type": device_type,
        "timestamp": timestamp,
        "measurement": measurement
    }


@api.post("/add_multiple/")
async def add_multiple(device_type: str, measurements: List[Dict]):
    if device_type not in devices:
        raise HTTPException(status_code=400, detail=f"Device type '{device_type}' not supported.")
    
    prepared_measurements = [(m["timestamp"], float(m["measurement"])) for m in measurements]
    devices[device_type].log_multiple(prepared_measurements)
    
    return {
        "message": f"{len(measurements)} measurements added successfully",
        "device_type": device_type,
        "measurements": measurements
    }


@api.get("/max_accumulated/")
async def max_accumulated(device_type: str):
    if device_type not in devices:
        raise HTTPException(status_code=400, detail=f"Device type '{device_type}' not supported.")
    
    output = devices[device_type].peak_accumulation()
    if len(output) < 3 or (output[0] == -1 and output[1] == -1):
        return {
            "max_accumulation": -1,
            "start": -1,
            "end": -1,
            "error": f"No data available for device type '{device_type}'.",
            "status": 404
        }
    
    return {
        "start": output[0],
        "end": output[1],
        "error": None,
        "status": 200
    }


if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8000)
