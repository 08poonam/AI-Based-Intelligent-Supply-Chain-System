import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pickle

df = pd.read_csv("logistics_data.csv")

# -------------------------
# Encode
# -------------------------
traffic_map = {"Low": 0, "Medium": 1, "High": 2}
weather_map = {"Clear": 0, "Rain": 1}
stock_map = {"Yes": 1, "No": 0}

df["traffic"] = df["traffic"].map(traffic_map)
df["weather"] = df["weather"].map(weather_map)
df["stock"] = df["stock"].map(stock_map)

# -------------------------
# 🚨 IMPORTANT FIX: CLEAN BEFORE SPLIT
# -------------------------
df = df.dropna().reset_index(drop=True)

# -------------------------
# Features & Targets (SAME DF)
# -------------------------
X = df[["distance", "traffic", "weather", "stock"]]
y_delay = df["delay"]
y_eta = df["eta"]

# -------------------------
# FINAL CHECK (IMPORTANT)
# -------------------------
print("X:", len(X))
print("y_delay:", len(y_delay))
print("y_eta:", len(y_eta))

# -------------------------
# SPLIT (AFTER ALIGNMENT)
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y_delay, test_size=0.2)

eta_X_train, eta_X_test, eta_y_train, eta_y_test = train_test_split(X, y_eta, test_size=0.2)

# -------------------------
# MODELS
# -------------------------
delay_model = RandomForestClassifier(n_estimators=200)
delay_model.fit(X_train, y_train)

eta_model = RandomForestRegressor(n_estimators=200)
eta_model.fit(eta_X_train, eta_y_train)

# -------------------------
# SAVE
# -------------------------
pickle.dump(delay_model, open("delay_model.pkl", "wb"))
pickle.dump(eta_model, open("eta_model.pkl", "wb"))

print("✅ Models trained successfully!")