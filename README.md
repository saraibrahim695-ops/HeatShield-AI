# 🌡️ HeatShield AI

### AI-Powered Heat Risk Prediction & Early Warning

HeatShield AI is a machine-learning application designed to help people understand and respond to dangerous heat conditions.

The application combines live weather data with a Random Forest machine-learning model to estimate heat risk and provide practical safety recommendations.

## 🚀 Features

- 🌡️ Live weather information
- 🤖 AI-powered heat-risk prediction
- 🔥 Heat-risk score from 0–100
- 📊 AI confidence score
- 🧠 Explanation of factors behind the prediction
- 💡 Practical safety recommendations
- 🌍 Support for 7 languages
- 📱 Web-based interface

## 🧠 How It Works

1. The user enters a city.
2. HeatShield AI retrieves live weather conditions.
3. Temperature, humidity, and wind data are processed.
4. The Random Forest model predicts the heat-risk level.
5. HeatShield AI generates a heat-risk score.
6. The application provides an explanation and safety recommendations.

## 🛠️ Technologies

- Python
- Streamlit
- Scikit-learn
- Random Forest
- OpenWeather API
- Joblib
- Requests

## 📁 Project Structure

```text
HeatShield-AI/
├── app.py
├── model.pkl
├── requirements.txt
├── README.md
└── .devcontainer/
