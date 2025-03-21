import irsdk
from flask import Flask, jsonify, render_template
import threading
import time

app = Flask(__name__)
ir = irsdk.IRSDK()
telemetry_data = {"speed_kmph": 0, "gear": 0, "rpm": 0}

def update_telemetry():
    global telemetry_data
    while True:
        if ir.is_initialized and ir.is_connected:
            # Convert speed to km/h
            telemetry_data["speed_kmph"] = ir['Speed'] * 3.6  # m/s to km/h
            telemetry_data["gear"] = ir['Gear']
            telemetry_data["rpm"] = ir['RPM']


        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(telemetry_data)

if __name__ == '__main__':
    ir.startup()  # Ensure to use startup to initialize
    threading.Thread(target=update_telemetry, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
