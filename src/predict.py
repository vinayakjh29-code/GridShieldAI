
import joblib
import pandas as pd

# Load trained AI model
model = joblib.load("models/gridshield_model.pkl")

# New network traffic
new_data = pd.DataFrame([{
    "packet_count": 1000,
    "traffic_volume": 50000,
    "connection_rate": 500,
    "port_number": 80
}])

# Predict traffic category
prediction = model.predict(new_data)

print("==============================")
print("       GRIDSHIELD AI")
print("==============================")

print("Traffic Analysis Completed!")
print("Predicted Category:", prediction[0])

if prediction[0] == "Normal":
    print("Status: NORMAL TRAFFIC")
else:
    print("Status: SUSPICIOUS TRAFFIC")
    print("Security Alert: CHECK REQUIRED")

print("==============================")
