import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
data = pd.read_csv('data/dataset.csv')

# Convert text to numbers
le = LabelEncoder()

data['Traffic'] = le.fit_transform(data['Traffic'])
data['Weather'] = le.fit_transform(data['Weather'])
data['Stock'] = le.fit_transform(data['Stock'])
data['Delay'] = le.fit_transform(data['Delay'])

# Features and Target
X = data[['Distance', 'Traffic', 'Weather', 'Stock']]
y = data['Delay']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open('model.pkl', 'wb'))

print("Model trained and saved successfully!")