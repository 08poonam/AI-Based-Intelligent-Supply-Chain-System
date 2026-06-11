# 🚀 AI-Based Intelligent Supply Chain System

An advanced supply chain optimization platform that leverages machine learning, real-time data analytics, and predictive insights to optimize logistics operations across India's major cities.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Integrations](#api-integrations)
- [Machine Learning Models](#machine-learning-models)
- [Database Schema](#database-schema)
- [Dashboard Features](#dashboard-features)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This system is designed to revolutionize supply chain management by providing:

- **Predictive Analytics**: ML-powered delay predictions and ETA calculations
- **Smart Warehouse Selection**: Automatic selection of optimal warehouse based on multiple factors
- **Real-time Decision Support**: Live traffic, weather, and inventory data integration
- **Interactive Dashboard**: User-friendly interface for order management and visualization
- **Route Optimization**: Intelligent routing considering distance, traffic, and weather conditions
- **Risk Assessment**: Comprehensive delivery risk analysis with actionable recommendations

## ✨ Features

### Core Functionality
- 🏭 **Automated Warehouse Selection**: Identifies the best warehouse for each order considering:
  - Stock availability
  - Distance from delivery location
  - Real-time traffic conditions
  - Weather patterns
  
- 🤖 **AI-Powered Predictions**:
  - Delay prediction using Random Forest Classification
  - ETA (Estimated Time of Arrival) estimation using Random Forest Regression
  - Confidence scoring for predictions

- 🌦️ **Real-time Data Integration**:
  - OpenWeatherMap API for weather conditions
  - OpenRouteService for accurate distance and travel time calculation
  - Dynamic traffic pattern analysis

- 📊 **Advanced Analytics**:
  - Delivery risk assessment (0-100 scale)
  - Speed analysis and efficiency metrics
  - Cost calculation per delivery
  - System load monitoring
  - Priority classification (High/Medium/Low)

- 💾 **Order History Management**:
  - Complete audit trail of all orders
  - Historical data analysis
  - Delivery status tracking

- 📈 **Decision Support Features**:
  - What-if analysis for traffic and weather scenarios
  - Alternative warehouse suggestions
  - Delivery recommendations based on risk factors
  - Detailed explanation of factors affecting delivery

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.x, Flask |
| **Frontend** | HTML5, JavaScript |
| **Database** | SQLite |
| **ML Framework** | Scikit-learn (Random Forest) |
| **APIs** | OpenWeatherMap, OpenRouteService |
| **Data Processing** | Pandas, NumPy |
| **Model Storage** | Pickle |

## 📂 Project Structure

```
AI-Based-Intelligent-Supply-Chain-System/
├── app.py                          # Main Flask application
├── train_model.py                  # Model training script
├── model.py                        # Model utility functions
├── test_model.py                   # Model testing
├── dataset_generator.py            # Dataset creation utility
├── database.db                     # SQLite database
├── logistics_data.csv              # Training dataset
├── delay_model.pkl                 # Trained delay prediction model
├── eta_model.pkl                   # Trained ETA estimation model
├── model.pkl                       # General model file
├── templates/                      # HTML templates
│   ├── index.html                  # Homepage/order form
│   ├── result.html                 # Prediction results page
│   ├── history.html                # Order history
│   ├── add_warehouse.html          # Add warehouse form
│   └── warehouses.html             # Warehouse list view
├── data/                           # Data directory
├── Project_Documentation.ipynb     # Detailed documentation
└── README.md                       # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/08poonam/AI-Based-Intelligent-Supply-Chain-System.git
cd AI-Based-Intelligent-Supply-Chain-System
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install flask
pip install pandas
pip install scikit-learn
pip install requests
```

### Step 4: Verify Installation
```bash
python -c "import flask, pandas, sklearn; print('All dependencies installed successfully!')"
```

## ⚙️ Configuration

### API Keys Setup

Edit `app.py` and configure your API keys:

```python
# Line 13-14 in app.py
API_KEY = "your_openweathermap_api_key"  # Get from openweathermap.org
ORS_API_KEY = "your_openrouteservice_key"  # Get from openrouteservice.org
```

### Database Initialization
The database is automatically initialized on first run. It creates two tables:
- **orders**: Stores all order predictions and results
- **warehouses**: Manages warehouse information and stock levels

### Supported Cities
The system supports 50+ Indian cities including:
- **Tier 1 Metro**: Delhi, Mumbai, Bangalore, Kolkata, Chennai, Hyderabad
- **Tier 2 Cities**: Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh
- **Regional Hubs**: Surat, Vadodara, Indore, Bhopal, and more

## 📖 Usage

### 1. Start the Application
```bash
python app.py
```
The application will run on `http://localhost:5000`

### 2. Train Models (Optional - if retraining)
```bash
python train_model.py
```
This trains both the delay prediction and ETA models and saves them as pickled files.

### 3. Access the Dashboard
Open your browser and navigate to `http://localhost:5000`

### 4. Place an Order
1. Select delivery city
2. Enter order quantity
3. Specify stock availability (Yes/No)
4. Click "Predict"

### 5. View Results
The system will display:
- Selected warehouse and distance
- Estimated delivery time
- Delay prediction with confidence score
- Risk assessment and recommendations
- Cost estimation
- Alternative warehouse options

### 6. Manage History
- View all past orders and predictions
- Delete individual orders or clear entire history
- Track delivery status and metrics

### 7. Warehouse Management
- Add new warehouses
- View warehouse list with stock levels
- Monitor warehouse capacity

## 🔗 API Integrations

### OpenWeatherMap API
```
Endpoint: http://api.openweathermap.org/data/2.5/weather
Purpose: Real-time weather data for delivery cities
```

### OpenRouteService API
```
Endpoint: https://api.openrouteservice.org/v2/directions/driving-car
Purpose: Distance and travel time calculation between cities
```

## 🧠 Machine Learning Models

### Delay Prediction Model
- **Algorithm**: Random Forest Classifier (200 estimators)
- **Features**: distance, traffic, weather, stock availability
- **Output**: Binary classification (Delay / No Delay)
- **Confidence**: Probability score (0-100%)

### ETA Estimation Model
- **Algorithm**: Random Forest Regressor (200 estimators)
- **Features**: distance, traffic, weather, stock availability
- **Output**: Delivery time in hours
- **Accuracy**: Based on historical logistics data

### Feature Encoding
```
Traffic:  Low=0, Medium=1, High=2
Weather:  Clear=0, Rain=1
Stock:    Yes=1, No=0
```

## 💾 Database Schema

### Orders Table
```sql
CREATE TABLE orders (
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
);
```

### Warehouses Table
```sql
CREATE TABLE warehouses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT,
    stock INTEGER
);
```

## 📊 Dashboard Features

### Prediction Results Page
- **Warehouse Information**: Selected warehouse name and location
- **Delivery Metrics**: 
  - Distance (km)
  - Travel time (hours)
  - Estimated cost
  - Delivery status
  
- **Risk Analysis**:
  - Risk score (0-100)
  - Risk factors explanation
  - Confidence level
  
- **Contextual Data**:
  - Weather conditions
  - Traffic status
  - System load
  - Stock availability
  
- **Advanced Features**:
  - What-if scenarios (high traffic, rainy conditions)
  - Alternative warehouse suggestions
  - Speed analysis
  - Personalized recommendations

## 🚀 Deployment

### Development Deployment
```bash
python app.py
```

### Production Deployment (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Heroku Deployment
```bash
git push heroku main
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Code Examples

### Making a Prediction
```python
from app import find_best_warehouse, calculate_delivery_real

warehouse, distance, travel_time = find_best_warehouse("Delhi", 50, "High")
delivery_time = calculate_delivery_real(travel_time, "High", "Clear")
```

### Accessing Warehouse Data
```python
from app import get_warehouses

warehouses = get_warehouses()
for w in warehouses:
    print(f"{w['name']} in {w['city']}: {w['stock']} units")
```

## 📚 Dataset Information

The system uses logistics data with the following features:
- **Distance**: Distance in kilometers between warehouses and delivery locations
- **Traffic**: Low, Medium, High
- **Weather**: Clear, Rain
- **Stock**: Available/Unavailable
- **Delay**: Binary target (0/1)
- **ETA**: Estimated time in hours

## 🐛 Troubleshooting

### Issue: API Key Errors
**Solution**: Verify API keys in `app.py` and check API quotas

### Issue: Database Errors
**Solution**: Delete `database.db` and restart the application to reinitialize

### Issue: Model Loading Errors
**Solution**: Run `python train_model.py` to retrain models

### Issue: City Not Found
**Solution**: Ensure city name matches exactly with `city_coords` dictionary in `app.py`

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your Contact Information]

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🎓 Educational Value

This project demonstrates:
- Machine Learning implementation with Scikit-learn
- Real-time API integration
- Database management with SQLite
- Web development with Flask
- Data processing with Pandas
- Full-stack application architecture

## 🙏 Acknowledgments

- OpenWeatherMap for weather data
- OpenRouteService for routing data
- Scikit-learn for ML libraries
- Flask framework community

---

**Last Updated**: June 2026  
**Version**: 1.0.0  
**Status**: Active Development

## 📈 Future Enhancements

- [ ] Multi-modal transportation support
- [ ] Advanced predictive analytics with deep learning
- [ ] Real-time delivery tracking
- [ ] Customer mobile app
- [ ] Blockchain integration for transparency
- [ ] Advanced reporting and BI tools
- [ ] Automated warehouse management
- [ ] Supply-demand forecasting

---

**Made with ❤️ for intelligent supply chain management**