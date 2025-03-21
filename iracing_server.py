import irsdk
from flask import Flask, jsonify, render_template
import threading
import time

app = Flask(__name__)
ir = irsdk.IRSDK()
telemetry_data = {
    "speed_kmph": 0,
    "gear": 0,
    "rpm": 0,
    "predicted_time": 0,
    "best_time": None,
    "car_dist_ahead": None,
    "car_dist_behind": None
}

def update_telemetry():
    global telemetry_data
    while True:
        if ir.is_initialized and ir.is_connected:
            telemetry_data["speed_kmph"] = ir.get_float("Speed", 0) * 3.6  # Convert to km/h
            telemetry_data["gear"] = ir.get_int("Gear", 0)
            telemetry_data["rpm"] = ir.get_int("RPM", 0)
            telemetry_data["predicted_time"] = ir.get_float("LapPredictedTime", 0)
            telemetry_data["best_time"] = ir.get_float("LapBestLapTime", 0)
            telemetry_data["car_dist_ahead"] = ir.get_float("CarIdxLapDistPct", None)
            telemetry_data["car_dist_behind"] = ir.get_float("CarIdxLapDistPct", None)

        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(telemetry_data)

if __name__ == '__main__':
    if not ir.startup():
        print("Failed to initialize iRSDK!")
        exit(1)
    
    threading.Thread(target=update_telemetry, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
