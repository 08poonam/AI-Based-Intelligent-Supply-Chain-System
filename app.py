from flask import Flask, render_template, request
import pickle
import requests
import sqlite3
import random
import math

app = Flask(__name__)

# -------------------------------
# 🔑 API KEY
# -------------------------------
API_KEY = "e318dc4b90bbfc0c03ab45a2218250f8"
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijk2YjcwMGZiNTU4NzRhYjNhYWM1NjdiM2ZkZDBlYzVmIiwiaCI6Im11cm11cjY0In0="

weather_cache = {}
distance_cache = {}

city_coords = {
    # Tier 1 metros
    "Delhi": [77.1025, 28.7041],
    "New Delhi": [77.2090, 28.6139],
    "Noida": [77.3910, 28.5355],
    "Greater Noida": [77.5500, 28.4744],
    "Gurgaon": [77.0266, 28.4595],
    "Faridabad": [77.3178, 28.4089],
    "Ghaziabad": [77.4538, 28.6692],
    "Sonipat": [77.0167, 28.9958],
    "Panipat": [76.9635, 29.3909],
    "Rohtak": [76.6115, 28.8955],
    "Meerut": [77.7064, 28.9845],
    "Bulandshahr": [77.8498, 28.4069],
    "Aligarh": [78.0880, 27.8974],
    "Mathura": [77.6737, 27.4924],
    "Mumbai": [72.8777, 19.0760],
    "Navi Mumbai": [73.0297, 19.0330],
    "Thane": [72.9781, 19.2183],
    "Kalyan": [73.1305, 19.2403],
    "Dombivli": [73.0866, 19.2183],
    "Panvel": [73.1100, 18.9894],
    "Vasai": [72.8058, 19.3919],
    "Virar": [72.7759, 19.4559],
    "Bangalore": [77.5946, 12.9716],
    "Chennai": [80.2707, 13.0827],
    "Hyderabad": [78.4867, 17.3850],   
    "Warangal": [79.5941, 17.9689],
    "Nizamabad": [78.0941, 18.6725],
    "Khammam": [80.1514, 17.2473],
    "Karimnagar": [79.1288, 18.4386],
    "Ramagundam": [79.4589, 18.7557],
    "Mahbubnagar": [77.9864, 16.7488],
    "Nalgonda": [79.2663, 17.0575],
    "Adilabad": [78.5320, 19.6641],
    "Siddipet": [78.8495, 18.1018],
    "Suryapet": [79.6205, 17.1405],
    "Jagtial": [78.9382, 18.7960],
    "Kolkata": [88.3639, 22.5726],

    # Western India
    "Pune": [73.8567, 18.5204],
    "Ahmedabad": [72.5714, 23.0225],
    "Surat": [72.8311, 21.1702],
    "Vadodara": [73.1812, 22.3072],

    # North India
    "Jaipur": [75.7873, 26.9124],
    "Lucknow": [80.9462, 26.8467],
    "Kanpur": [80.3319, 26.4499],
    "Chandigarh": [76.7794, 30.7333],

    # South India
    "Coimbatore": [76.9558, 11.0168],
    "Kochi": [76.2673, 9.9312],
    "Mysore": [76.6394, 12.2958],

    # Central India
    "Bhopal": [77.4126, 23.2599],
    "Indore": [75.8577, 22.7196],

    # East India
    "Patna": [85.1376, 25.5941],
    "Bhubaneswar": [85.8245, 20.2961]
}
# -------------------------------
# 🧠 INIT DATABASE
# -------------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            warehouse TEXT,
            distance REAL,
            delivery_time REAL,
            prediction TEXT,
            confidence REAL,
            risk INTEGER,
            weather TEXT,
            traffic TEXT,
            stock TEXT,
            city TEXT
        )
    ''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS warehouses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT,
    stock INTEGER
)
''')

    conn.commit()
    conn.close()

init_db()

# -------------------------------
# 🤖 LOAD MODEL
# -------------------------------
delay_model = pickle.load(open('delay_model.pkl', 'rb'))
eta_model = pickle.load(open('eta_model.pkl', 'rb'))

def ai_encode(traffic, weather, stock):
    return (
        {"Low": 0, "Medium": 1, "High": 2}[traffic],
        {"Clear": 0, "Rain": 1}[weather],
        {"Yes": 1, "No": 0}[stock]
    )

# -------------------------------
# 🏭 REAL WAREHOUSES
# -------------------------------
def get_real_distance(origin_city, destination_city):
    key = (origin_city, destination_city)

    # ✅ return cached result if exists
    if key in distance_cache:
        return distance_cache[key]
    try:
        url = "https://api.openrouteservice.org/v2/directions/driving-car"

        headers = {
            "Authorization": ORS_API_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [
                city_coords[origin_city],
                city_coords[destination_city]
            ]
        }

        response = requests.post(url, json=body, headers=headers)
        data = response.json()

        distance = data["routes"][0]["summary"]["distance"] / 1000  # km
        duration = data["routes"][0]["summary"]["duration"] / 3600   # hours

        result = (round(distance, 2), round(duration, 2))

        # ✅ store in cache
        distance_cache[key] = result

        return result

    except:
        return 999, 10
    
def get_warehouses():
    conn = sqlite3.connect('database.db')
    rows = conn.execute("SELECT name, city, stock FROM warehouses").fetchall()
    conn.close()

    return [{"name": r[0], "city": r[1], "stock": r[2]} for r in rows]

# -------------------------------
# 🌍 DISTANCE MATRIX
# -------------------------------
# city_distances = {
#     "Mumbai": {"Mumbai": 5, "Pune": 150, "Delhi": 1400, "Bangalore": 980},
#     "Pune": {"Mumbai": 150, "Pune": 5, "Delhi": 1300, "Bangalore": 840},
#     "Delhi": {"Mumbai": 1400, "Pune": 1300, "Delhi": 5, "Bangalore": 2100},
#     "Bangalore": {"Mumbai": 980, "Pune": 840, "Delhi": 2100, "Bangalore": 5}
# }

# -------------------------------
# 🌦️ WEATHER API
# -------------------------------
def get_weather(city):
        # ✅ return cached result if exists
    if city in weather_cache:
        return weather_cache[city]
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        data = requests.get(url).json()
        weather = data['weather'][0]['main']
        result = "Rain" if weather in ['Rain', 'Thunderstorm'] else "Clear"
        weather_cache[city] = result

        return result
    except:
        return "Clear"

# -------------------------------
# 🚦 AUTO TRAFFIC
# -------------------------------
def auto_traffic():
    return random.choice(["Low", "Medium", "High"])

# -------------------------------
# 🔄 ENCODING
# -------------------------------
def encode_input(traffic, weather, stock):
    return (
        {'Low': 0, 'Medium': 1, 'High': 2}[traffic],
        {'Clear': 0, 'Rain': 1}[weather],
        {'Yes': 1, 'No': 0}[stock]
    )

# -------------------------------
# 🚚 ROUTE OPTIMIZATION
# -------------------------------
def route_score(distance, traffic):
    score = distance

    if traffic == "High":
        score += 100
    elif traffic == "Medium":
        score += 50

    return score

def find_best_warehouse(order_city, order_qty, traffic):
    best = None
    best_score = float('inf')

    same_city_warehouse = None

    for w in get_warehouses():

        if w["stock"] >= order_qty:

            distance, travel_time = get_real_distance(order_city, w["city"])

            if w["city"].lower() == order_city.lower():
                same_city_warehouse = (w, distance, travel_time)

            score = route_score(distance, traffic)

            if score < best_score:
                best_score = score
                best = (w, distance, travel_time)

    if same_city_warehouse:
        return same_city_warehouse

    return best if best else (None, 999, 10)
# -------------------------------
# 🚚 DELIVERY
# -------------------------------
def calculate_delivery(distance, traffic, weather, stock):
    time = distance / 40

    if traffic == "High": time += 2
    elif traffic == "Medium": time += 1

    if weather == "Rain": time += 1

    return round(time, 2), "Calculated"

def calculate_delivery_real(travel_time, traffic, weather):
    time = travel_time

    if traffic == "High":
        time += 1.5
    elif traffic == "Medium":
        time += 0.7

    if weather == "Rain":
        time += 1

    return round(time, 2)
# -------------------------------
# 📊 EXTRA FEATURES
# -------------------------------
def calculate_risk(t, w, s):
    risk = (40 if t=="High" else 20 if t=="Medium" else 0)
    if w == "Rain": risk += 30
    if s == "No": risk += 50
    return min(risk, 100)

def eta_category(t):
    return "Fast" if t < 2 else "Moderate" if t < 4 else "Slow"

def what_if(distance, weather, stock):
    ht,_ = calculate_delivery(distance,"High",weather,stock)
    rt,_ = calculate_delivery(distance,"Medium","Rain",stock)
    return ht, rt

def explain(traffic, weather, stock, distance, risk):
    explanation = []

    if traffic == "High":
        explanation.append("Heavy traffic congestion is slowing delivery routes.")

    if weather == "Rain":
        explanation.append("Adverse weather conditions are impacting travel speed.")

    if stock == "No":
        explanation.append("Stock unavailability may cause dispatch delay.")

    if distance > 1000:
        explanation.append("Long distance increases delivery time.")

    if risk > 70:
        explanation.append("Overall delivery risk is high due to combined factors.")

    if not explanation:
        return "All conditions are optimal for smooth delivery."

    return " ".join(explanation)

def get_priority(q):
    return "High" if q > 50 else "Medium" if q > 20 else "Low"

def system_load():
    conn = sqlite3.connect('database.db')
    count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    conn.close()
    return "High" if count > 15 else "Medium" if count > 5 else "Low"

def calculate_cost(distance):
    return round(distance * 5, 2)

def delivery_status(t):
    return "On Time" if t < 2 else "At Risk" if t < 4 else "Delayed"

def alt_warehouse(order_city, qty, current):
    alt=[]
    for w in get_warehouses():
        if w["name"] != current and w["stock"] >= qty:
            dist, _ = get_real_distance(order_city, w["city"])
            alt.append((w["name"], dist))

    alt.sort(key=lambda x: x[1])
    return alt[0][0] if alt else "None"

def recommendation(risk, traffic, weather):
    if risk > 70:
        return "Consider rerouting or delaying shipment."
    elif traffic == "High":
        return "Try alternate delivery route."
    elif weather == "Rain":
        return "Allow buffer time for weather delays."
    return "No action needed."

def speed_analysis(distance, time):
    speed = distance / time if time > 0 else 0

    if speed > 40:
        return "Fast route with minimal delay."
    elif speed > 25:
        return "Moderate delivery speed."
    return "Slow delivery due to conditions."
# -------------------------------
# 🌐 ROUTES
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    order_city = request.form['city']
    qty = int(request.form['quantity'])
    stock = request.form['stock']

    weather = get_weather(order_city)
    traffic = auto_traffic()

    wh, distance, travel_time = find_best_warehouse(order_city, qty, traffic)
    # -------------------------
    # 🧠 AI PREDICTION BLOCK (ADD HERE)
    # -------------------------

    t, w, s = ai_encode(traffic, weather, stock)

    features = [[distance, t, w, s]]

    delay_pred = delay_model.predict(features)[0]
    eta_pred = eta_model.predict(features)[0]

   # result = "Delay" if delay_pred == 1 else "No Delay"

    # ❌ NO WAREHOUSE
    if wh is None:
        return render_template(
            'result.html',
            error="No warehouse available",
            suggestion="Reduce quantity or change city",
            warehouse="N/A",
            delivery_time=0,
            prediction="N/A",
            confidence=0,
            risk=0,
            eta="N/A",
            alt_warehouse="N/A",
            high_traffic_time=0,
            rain_time=0,
            explanation="N/A",
            weather=weather,
            traffic=traffic,
            cost=0,
            priority="N/A",
            status="Failed",
            load=system_load(),
            city=order_city,
            remaining_stock=0,
            recommendation = recommendation(0, traffic, weather),
            distance=distance,
            speed_info = speed_analysis(0, 0)
        )

    # ✅ NORMAL
    wname = wh["name"]

    if math.isinf(distance) or distance > 10000:
        distance = 999

    # 📦 UPDATE STOCK
    wh["stock"] -= qty

    dtime = calculate_delivery_real(travel_time, traffic, weather)

    t,w,s = encode_input(traffic, weather, stock)
    features = [[distance, t, w, s]]

    delay_pred = delay_model.predict(features)[0]
    eta_pred = eta_model.predict(features)[0]

    result = "Delay" if delay_pred == 1 else "No Delay"
    #conf = round(max(prob[0]) * 100, 2)
    conf = round(max(delay_model.predict_proba(features)[0]) * 100, 2)
    risk = calculate_risk(traffic, weather, stock)
    eta = eta_category(dtime)

    alt = alt_warehouse(order_city, qty, wname)
    ht, rt = what_if(distance, weather, stock)
    explanation = explain(traffic, weather, stock,distance,risk)

    cost = calculate_cost(distance)
    priority = get_priority(qty)
    status = delivery_status(dtime)
    load = system_load()

    # 💾 SAVE
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders 
        (warehouse, distance, delivery_time, prediction, confidence, risk, weather, traffic, stock, city)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (wname, distance, dtime, result, conf, risk, weather, traffic, stock, order_city))

    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        warehouse=wname,
        delivery_time=dtime,
        prediction=result,
        confidence=conf,
        risk=risk,
        eta=eta,
        alt_warehouse=alt,
        high_traffic_time=ht,
        rain_time=rt,
        explanation=explanation,
        weather=weather,
        traffic=traffic,
        cost=cost,
        priority=priority,
        status=status,
        load=load,
        city=order_city,
        remaining_stock=wh["stock"],       
        recommendation = recommendation(risk, traffic, weather),
        distance=distance,
        speed_info = speed_analysis(distance, dtime)
    )

@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('history.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return "<script>window.location.href='/history'</script>"

@app.route('/delete_all')
def delete_all():
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM orders")
    conn.commit()
    conn.close()
    return "<script>window.location.href='/history'</script>"

@app.route('/add_warehouse', methods=['GET', 'POST'])
def add_warehouse():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        stock = int(request.form['stock'])

        conn = sqlite3.connect('database.db')
        conn.execute(
            "INSERT INTO warehouses (name, city, stock) VALUES (?, ?, ?)",
            (name, city, stock)
        )
        conn.commit()
        conn.close()

        return "<script>alert('Warehouse Added');window.location.href='/'</script>"

    return render_template('add_warehouse.html')

@app.route('/warehouses')
def view_warehouses():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM warehouses").fetchall()
    conn.close()

    return render_template('warehouses.html', data=data)
# -------------------------------
# ▶️ RUN
# -------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)