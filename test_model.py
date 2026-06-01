import pickle

model = pickle.load(open('model.pkl', 'rb'))

# Example input:
# Distance=40, Traffic=High(2), Weather=Rain(1), Stock=No(0)
prediction = model.predict([[40, 2, 1, 0]])

print("Delay Prediction:", prediction)