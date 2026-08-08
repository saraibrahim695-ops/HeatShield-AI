
import os
import joblib
import requests
import streamlit as st

# ==========================================
# HEATSHIELD AI
# ==========================================

st.set_page_config(
      page_title="HeatShield AI",
          page_icon="🌡️",
              layout="centered"
              )

# ==========================================
# LOAD MODEL
# ==========================================

try:
    model = joblib.load("model.pkl")
except Exception as e:
    st.error("Could not load model.pkl")
    st.stop()


# ==========================================
# API KEY
# ==========================================

# For Streamlit Cloud:
# Add OPENWEATHER_API_KEY in App Settings > Secrets
#
# For local testing:
# You can temporarily set an environment variable.

API_KEY = os.getenv("OPENWEATHER_API_KEY")

try:
    if not API_KEY:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except Exception:
    pass


# ==========================================
# GET LIVE WEATHER
# ==========================================

def get_weather(city):

    if not API_KEY:
        return None, "OpenWeather API key is missing."

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None, "City not found or weather service unavailable."

        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        # OpenWeather gives wind in m/s.
        # Our model was trained using km/h.
        wind_ms = data["wind"]["speed"]
        wind_kmh = wind_ms * 3.6

        return {
              "temperature": temperature,
                  "humidity": humidity,
                      "wind_ms": wind_ms,
                          "wind_kmh": wind_kmh,
                              "latitude": data["coord"]["lat"],
                                  "longitude": data["coord"]["lon"],
                                      "location_name": data["name"],
                                          "country": data["sys"]["country"]
                                          }, None


    except requests.RequestException:
        return None, "Unable to connect to the weather service."


# ==========================================
# HEAT SCORE
# ==========================================

def calculate_heat_score(temp, humidity, wind_ms):

    score = (
        (temp * 1.5)
        + (humidity * 0.4)
        - (wind_ms * 2)
    )

    score = max(0, min(100, int(score)))

    return score


# ==========================================
# RISK INFORMATION
# ==========================================

def get_risk_info(prediction):

    if prediction == "Low":

        return (
            "🟢",
            "LOW",
            "Stay hydrated and enjoy normal outdoor activities.",
            "success"
        )

    elif prediction == "Moderate":

        return (
            "🟡",
            "MODERATE",
            "Drink water regularly, take breaks in the shade, "
            "and avoid prolonged exposure to direct sunlight.",
            "warning"
        )

    elif prediction == "High":

        return (
            "🟠",
            "HIGH",
            "Limit outdoor activity, stay in shaded areas, "
            "drink water frequently, and take regular breaks.",
            "warning"
        )

    else:

        return (
            "🔴",
            "EXTREME",
            "Avoid prolonged outdoor exposure and stay in a cool "
            "or air-conditioned environment.",
            "error"
        )


# ==========================================
# EXPLAIN PREDICTION
# ==========================================

def explain_prediction(temp, humidity, wind_ms):

    reasons = []

    if temp >= 40:
        reasons.append("🌡️ Very high temperature")

    elif temp >= 38:
        reasons.append("🌡️ High temperature")

    if humidity >= 70:
        reasons.append("💧 High humidity")

    if wind_ms <= 5:
        reasons.append("🌬️ Low wind speed provides less cooling")

    if not reasons:
        reasons.append("✅ No major heat-related weather factor detected.")

    return reasons


# ==========================================
# MAIN PREDICTION
# ==========================================

def predict_city(city):

    weather, error = get_weather(city)

    if error:
        return None, error

    temperature = weather["temperature"]
    humidity = weather["humidity"]
    wind_ms = weather["wind_ms"]
    wind_kmh = weather["wind_kmh"]

    # IMPORTANT:
    # The trained model expects:
    # Temperature (C), Humidity, Wind Speed (km/h)

    features = [[temperature, humidity, wind_kmh]]

    prediction = model.predict(features)[0]

    # Confidence
    try:
        probabilities = model.predict_proba(features)[0]
        confidence = max(probabilities) * 100
    except Exception:
        confidence = 0

    score = calculate_heat_score(
        temperature,
        humidity,
        wind_ms
    )

    emoji, risk_name, advice, alert_type = get_risk_info(prediction)

    reasons = explain_prediction(
        temperature,
        humidity,
        wind_ms
    )

    return {
        "temperature": temperature,
        "humidity": humidity,
        "wind_ms": wind_ms,
        "wind_kmh": wind_kmh,
        "prediction": prediction,
        "confidence": confidence,
        "score": score,
        "emoji": emoji,
        "risk_name": risk_name,
        "advice": advice,
        "alert_type": alert_type,
        "reasons": reasons
    }, None


# ==========================================
# USER INTERFACE
# ==========================================

st.title("🌡️ HeatShield AI")

st.subheader("AI-Powered Heat Risk Prediction")

st.write(
    "Enter a city to retrieve live weather conditions "
    "and estimate heat risk using a machine-learning model."
)

city = st.text_input(
    "🌍 Enter City",
    placeholder="Example: Abu Dhabi"
)

predict_button = st.button(
    "🔍 Analyze Heat Risk",
    type="primary"
)


# ==========================================
# RUN PREDICTION
# ==========================================

if predict_button:

    if not city.strip():

        st.warning("Please enter a city name.")

    else:

        with st.spinner("Getting live weather and analyzing risk..."):

            result, error = predict_city(city.strip())

            if error:

                st.error(error)

            else:

                st.divider()

                # ----------------------------------
                # WEATHER
                # ----------------------------------

                st.subheader(
                      f"📍 {city.strip().title()}"
                      )


                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "🌡️ Temperature",
                        f"{result['temperature']:.1f} °C"
                    )

                with col2:
                    st.metric(
                        "💧 Humidity",
                        f"{result['humidity']:.0f}%"
                    )

                with col3:
                    st.metric(
                        "🌬️ Wind",
                        f"{result['wind_ms']:.1f} m/s"
                    )

                st.divider()

                # ----------------------------------
                # RISK
                # ----------------------------------

                st.subheader("🔥 Heat Risk")

                st.metric(
                    "Heat Score",
                    f"{result['score']}/100"
                )

                st.progress(
                    result["score"] / 100
                )

                st.markdown(
                    f"## {result['emoji']} {result['risk_name']}"
                )

                st.write(
                    f"**AI Prediction:** {result['prediction']}"
                )

                st.write(
                    f"**AI Confidence:** "
                    f"{result['confidence']:.1f}%"
                )

                # ----------------------------------
                # ALERT
                # ----------------------------------

                if result["prediction"] == "Extreme":

                    st.error(
                        "🚨 EXTREME HEAT ALERT\n\n"
                        "Avoid prolonged outdoor exposure "
                        "and stay in a cool environment."
                    )

                elif result["prediction"] == "High":

                    st.warning(
                        "⚠️ HIGH HEAT RISK\n\n"
                        "Limit prolonged outdoor activity "
                        "and take regular cooling breaks."
                    )

                elif result["prediction"] == "Moderate":

                    st.warning(
                        "🟡 MODERATE HEAT RISK\n\n"
                        "Stay hydrated and take regular breaks."
                    )

                else:

                    st.success(
                        "🟢 LOW HEAT RISK"
                    )

                # ----------------------------------
                # EXPLANATION
                # ----------------------------------

                st.subheader("🧠 Why did the AI predict this?")

                for reason in result["reasons"]:
                    st.write(reason)

                # ----------------------------------
                # RECOMMENDATIONS
                # ----------------------------------

                st.subheader("💡 Safety Recommendations")

                st.write(result["advice"])

                # ----------------------------------
                # MODEL INFORMATION
                # ----------------------------------

                with st.expander("🤖 About the AI"):

                    st.write(
                        "HeatShield AI uses a Random Forest "
                        "machine-learning model trained using "
                        "weather observations containing "
                        "temperature, humidity, and wind speed."
                    )

                    st.write(
                        "The system combines the model prediction "
                        "with a heat-risk score and live weather "
                        "information to provide an understandable "
                        "risk assessment."
                    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "HeatShield AI • AI-powered heat risk awareness"
)
