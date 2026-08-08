
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
# LANGUAGE SUPPORT
# ==========================================

LANGUAGES = {
    "English": "en",
    "العربية": "ar",
    "Español": "es",
    "Français": "fr",
    "हिन्दी": "hi",
    "اردو": "ur",
    "中文": "zh"
}

language_name = st.sidebar.selectbox(
    "🌐 Language",
    list(LANGUAGES.keys())
)

language = LANGUAGES[language_name]
# ==========================================
# TRANSLATIONS
# ==========================================

TEXT = {
    "en": {
    "title": "🌡️ HeatShield AI",
    "subtitle": "AI-Powered Heat Risk Prediction & Early Warning",
    "description": "Protecting people from dangerous heat with AI.",
    "city": "🌍 Enter City",
    "button": "🔍 Analyze Heat Risk",
    "temperature": "🌡️ Temperature",
    "humidity": "💧 Humidity",
    "wind": "🌬️ Wind",
    "heat_risk": "🔥 Heat Risk",
    "heat_score": "Heat Score",
    "prediction": "AI Prediction",
    "confidence": "AI Confidence",
    "why": "🧠 Why did the AI predict this?",
    "recommendations": "💡 Safety Recommendations",
    "about": "🤖 About the AI",
    "low": "LOW",
    "moderate": "MODERATE",
    "high": "HIGH",
    "extreme": "EXTREME",
    "low_advice": "Stay hydrated and enjoy normal outdoor activities.",
    "moderate_advice": "Drink water regularly, take breaks in the shade, and avoid prolonged exposure to direct sunlight.",
    "high_advice": "Limit outdoor activity, stay in shaded areas, drink water frequently, and take regular breaks.",
    "extreme_advice": "Avoid prolonged outdoor exposure and stay in a cool or air-conditioned environment.",
    "source": "Source: OpenWeather"
     },

    "ar": {
    "title": "🌡️ HeatShield AI",
    "subtitle": "التنبؤ بمخاطر الحرارة والإنذار المبكر بالذكاء الاصطناعي",
    "description": "حماية الناس من الحرارة الخطرة باستخدام الذكاء الاصطناعي.",
    "city": "🌍 أدخل اسم المدينة",
    "button": "🔍 تحليل مخاطر الحرارة",
    "temperature": "🌡️ درجة الحرارة",
    "humidity": "💧 الرطوبة",
    "wind": "🌬️ سرعة الرياح",
    "heat_risk": "🔥 مخاطر الحرارة",
    "heat_score": "درجة الحرارة الخطرة",
    "prediction": "توقع الذكاء الاصطناعي",
    "confidence": "ثقة الذكاء الاصطناعي",
    "why": "🧠 لماذا توقع الذكاء الاصطناعي ذلك؟",
    "recommendations": "💡 إرشادات السلامة",
    "about": "🤖 حول الذكاء الاصطناعي",
    "low": "منخفض",
    "moderate": "متوسط",
    "high": "مرتفع",
    "extreme": "شديد",
    "low_advice": "حافظ على ترطيب جسمك ويمكنك ممارسة الأنشطة الخارجية بشكل طبيعي.",
    "moderate_advice": "اشرب الماء بانتظام وخذ فترات راحة في الظل وتجنب التعرض الطويل لأشعة الشمس المباشرة.",
    "high_advice": "قلل من الأنشطة الخارجية والبقاء تحت الشمس، واشرب الماء بشكل متكرر وخذ فترات راحة.",
    "extreme_advice": "تجنب التعرض الطويل للحرارة والبقاء في مكان بارد أو مكيف.",
    "source": "المصدر: OpenWeather"
        },

    "es": {
    "title": "🌡️ HeatShield AI",
    "subtitle": "Predicción del riesgo de calor y alerta temprana con IA",
    "description": "Protegiendo a las personas del calor peligroso mediante IA.",
    "city": "🌍 Introduce una ciudad",
    "button": "🔍 Analizar riesgo de calor",
    "temperature": "🌡️ Temperatura",
    "humidity": "💧 Humedad",
    "wind": "🌬️ Viento",
    "heat_risk": "🔥 Riesgo de calor",
    "heat_score": "Puntuación de calor",
    "prediction": "Predicción de IA",
    "confidence": "Confianza de la IA",
    "why": "🧠 ¿Por qué la IA hizo esta predicción?",
    "recommendations": "💡 Recomendaciones de seguridad",
    "about": "🤖 Sobre la IA",
    "source": "Fuente: OpenWeather"
        },

    "fr": {
    "title": "🌡️ HeatShield AI",
    "subtitle": "Prédiction du risque de chaleur et alerte précoce par IA",
    "description": "Protéger les personnes contre les fortes chaleurs grâce à l'IA.",
    "city": "🌍 Entrez une ville",
    "button": "🔍 Analyser le risque de chaleur",
    "temperature": "🌡️ Température",
    "humidity": "💧 Humidité",
    "wind": "🌬️ Vent",
    "heat_risk": "🔥 Risque de chaleur",
    "heat_score": "Score de chaleur",
    "prediction": "Prédiction de l'IA",
    "confidence": "Confiance de l'IA",
    "why": "🧠 Pourquoi l'IA a-t-elle fait cette prédiction ?",
    "recommendations": "💡 Recommandations de sécurité",
    "about": "🤖 À propos de l'IA",
    "source": "Source : OpenWeather"
        },

    "hi": {
    "title": "🌡️ HeatShield AI",
    "subtitle": "AI द्वारा गर्मी के जोखिम का अनुमान और प्रारंभिक चेतावनी",
    "description": "AI की मदद से लोगों को खतरनाक गर्मी से बचाना।",
    "city": "🌍 शहर का नाम दर्ज करें",
    "button": "🔍 गर्मी के जोखिम का विश्लेषण करें",
    "temperature": "🌡️ तापमान",
    "humidity": "💧 नमी",
    "wind": "🌬️ हवा",
    "heat_risk": "🔥 गर्मी का जोखिम",
    "heat_score": "हीट स्कोर",
    "prediction": "AI अनुमान",
    "confidence": "AI विश्वास",
    "why": "🧠 AI ने यह अनुमान क्यों लगाया?",
    "recommendations": "💡 सुरक्षा सुझाव",
    "about": "🤖 AI के बारे में",
    "source": "स्रोत: OpenWeather"
        },

    "ur": {
    "title": "🌡️ HeatShield AI",
    "subtitle": "مصنوعی ذہانت سے گرمی کے خطرے کی پیش گوئی اور ابتدائی انتباہ",
    "description": "مصنوعی ذہانت کے ذریعے لوگوں کو خطرناک گرمی سے محفوظ رکھنا۔",
    "city": "🌍 شہر کا نام درج کریں",
    "button": "🔍 گرمی کے خطرے کا تجزیہ کریں",
    "temperature": "🌡️ درجہ حرارت",
    "humidity": "💧 نمی",
    "wind": "🌬️ ہوا",
    "heat_risk": "🔥 گرمی کا خطرہ",
    "heat_score": "ہیٹ اسکور",
    "prediction": "AI پیش گوئی",
    "confidence": "AI اعتماد",
    "why": "🧠 AI نے یہ پیش گوئی کیوں کی؟",
    "recommendations": "💡 حفاظتی تجاویز",
    "about": "🤖 AI کے بارے میں",
    "source": "ماخذ: OpenWeather"
        },

    "zh": {
    "title": "🌡️ HeatShield AI",
    "subtitle": "AI 热风险预测与预警",
    "description": "利用人工智能帮助人们预防危险高温。",
    "city": "🌍 输入城市",
    "button": "🔍 分析热风险",
    "temperature": "🌡️ 温度",
    "humidity": "💧 湿度",
    "wind": "🌬️ 风速",
    "heat_risk": "🔥 热风险",
    "heat_score": "热风险评分",
    "prediction": "AI 预测",
    "confidence": "AI 置信度",
    "why": "🧠 AI 为什么做出这个预测？",
    "recommendations": "💡 安全建议",
    "about": "🤖 关于 AI",
    "source": "来源：OpenWeather"
        }
}

T = TEXT[language]

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
        f"?q={city},AE&appid={API_KEY}&units=metric"
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

st.title(T["title"])
st.subheader(T["subtitle"])

st.markdown(
    f"""
        **{T["description"]}**

            HeatShield AI combines live weather data with machine learning
                to estimate heat risk and provide practical safety guidance.
                    """
                    )

st.write(
    "Enter a city to retrieve live weather conditions "
    "and estimate heat risk using a machine-learning model."
)

city = st.text_input(
      T["city"],
          placeholder="Abu Dhabi"
          )

predict_button = st.button(
      T["button"],
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
                            T["temperature"],
                                    f"{result['temperature']:.1f} °C"
                                        )
                st.caption(T["source"])

                with col2:
                    st.metric(
                            T["humidity"],
                                    f"{result['humidity']:.0f}%"
                                        )

                with col3:
                    st.metric(
                            T["wind"],
                                    f"{result['wind_ms']:.1f} m/s"
                                        )
                st.divider()

                # ----------------------------------
                # RISK
                # ----------------------------------

                st.subheader(T["heat_risk"])

                st.metric(
                            T["heat_score"],
                                f"{result['score']}/100"
                                )

                st.progress(
                    result["score"] / 100
                )

                st.markdown(
                    f"## {result['emoji']} {result['risk_name']}"
                )

                translated_prediction = T.get(
                      result["prediction"].lower(),
                          result["prediction"]
                          )

                st.write(
                              f"**{T['prediction']}:** {translated_prediction}"
                              )

                st.write(
                        f"**{T['confidence']}:** "
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
