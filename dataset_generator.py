import random
import pandas as pd

traffic_map = ["Low", "Medium", "High"]
weather_map = ["Clear", "Rain"]
stock_map = ["Yes", "No"]

data = []

for _ in range(5000):
    distance = random.randint(5, 2000)
    traffic = random.choice(traffic_map)
    weather = random.choice(weather_map)
    stock = random.choice(stock_map)

    # encode logic (target creation)
    delay_risk = 0

    if traffic == "High":
        delay_risk += 2
    elif traffic == "Medium":
        delay_risk += 1

    if weather == "Rain":
        delay_risk += 2

    if stock == "No":
        delay_risk += 3

    if distance > 1000:
        delay_risk += 1

    delay = 1 if delay_risk >= 4 else 0

    eta = (distance / 60) + delay_risk * 0.5

    data.append([distance, traffic, weather, stock, delay, eta])

df = pd.DataFrame(data, columns=[
    "distance", "traffic", "weather", "stock", "delay", "eta"
])

df = df.dropna()   # 🔥 ADD THIS

df.to_csv("logistics_data.csv", index=False)

print("Dataset created!")