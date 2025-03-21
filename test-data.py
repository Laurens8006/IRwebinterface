from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# Base telemetry data for a GT3 lap at Spa
telemetry_lap_data = [
    {"location": "La Source", "speed_kmph": 1, "gear": 2, "rpm": 4000},
    {"location": "La Source", "speed_kmph": 2, "gear": 2, "rpm": 4000},
    {"location": "La Source", "speed_kmph": 3, "gear": 2, "rpm": 4000},
    {"location": "Eau Rouge Entry", "speed_kmph": 0, "gear": 4, "rpm": 6000},
    {"location": "Raidillon Exit", "speed_kmph": 0, "gear": 5, "rpm": 7200},
    {"location": "Kemmel Straight", "speed_kmph": 0, "gear": 6, "rpm": 7800},
    {"location": "Les Combes Entry", "speed_kmph": 0, "gear": 4, "rpm": 6500},
    {"location": "Les Combes Exit", "speed_kmph": 14, "gear": 3, "rpm": 5500},
    {"location": "Bruxelles", "speed_kmph": 10, "gear": 2, "rpm": 4500},
    {"location": "Pouhon Entry", "speed_kmph": 16, "gear": 4, "rpm": 6200},
    {"location": "Pouhon Exit", "speed_kmph": 19, "gear": 5, "rpm": 7000},
    {"location": "Stavelot", "speed_kmph": 200, "gear": 5, "rpm": 7200},
    {"location": "Blanchimont", "speed_kmph": 250, "gear": 6, "rpm": 7800},
    {"location": "Bus Stop Chicane", "speed_kmph": 120, "gear": 3, "rpm": 5000},
    {"location": "Finish Straight", "speed_kmph": 270, "gear": 6, "rpm": 8000}
]

lap_index = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_telemetry():
    global lap_index
    base_data = telemetry_lap_data[lap_index]
    
    # Introduce dynamic variation
    speed_variation = random.randint(-5, 5)
    rpm_variation = random.randint(-200, 200)
    new_speed = max(50, base_data["speed_kmph"] + speed_variation)
    new_rpm = max(3000, base_data["rpm"] + rpm_variation)
    
    # Gear change logic (simulate upshift/downshift within realistic range)
    new_gear = base_data["gear"]
    if speed_variation > 3 and new_gear < 6:
        new_gear += 1
    elif speed_variation < -3 and new_gear > 2:
        new_gear -= 1
    
    telemetry = {
        "location": base_data["location"],
        "speed_kmph": new_speed,
        "gear": new_gear,
        "rpm": new_rpm
    }
    
    lap_index = (lap_index + 1) % len(telemetry_lap_data)  # Loop through the lap
    return jsonify(telemetry)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)