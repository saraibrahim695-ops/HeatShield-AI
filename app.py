import os
import joblib
import requests
import streamlit as st
# ==========================================
# HEATSHEILD AI
# ==========================================
with open('app.py', 'r') as f:
      app_content = f.read()
      print(app_content)
# ==========================================
# CENTERED DESIGN
# ==========================================

st.html("""
<style>

.main .block-container {
    max-width: 900px;
    margin: auto;
}

/* Center headings */
h1, h2, h3, h4, h5, h6 {
    text-align: center !important;
}

/* Center normal text */
.stMarkdown {
    text-align: center !important;
}

/* Center captions */
.stCaption {
    text-align: center !important;
}

/* Center metrics */
[data-testid="stMetric"] {
    text-align: center !important;
}

[data-testid="stMetricLabel"] {
    justify-content: center !important;
}

[data-testid="stMetricValue"] {
    justify-content: center !important;
}

/* Center buttons */
.stButton {
    display: flex;
    justify-content: center;
}

/* Center progress bar */
[data-testid="stProgress"] {
    margin-left: auto;
    margin-right: auto;
}

</style>
""")

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
      "🌍 Language",
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
    "intro": "Enter a city to retrieve live weather conditions and estimate heat risk using a machine-learning model.",
    "spinner": "Getting live weather and analyzing risk...",
    "empty_city": "Please enter a city name.",
    "alert_low": "LOW HEAT RISK",
    "alert_moderate": "MODERATE HEAT RISK",
    "alert_high": "HIGH HEAT RISK",
    "alert_extreme": "EXTREME HEAT ALERT",
    "about_text": "HeatShield AI uses a Random Forest machine-learning model trained using weather observations containing temperature, humidity, and wind speed.",
    "about_text2": "The system combines the model prediction with a heat-risk score and live weather information to provide an understandable risk assessment.",
    "footer": "HeatShield AI • AI-powered heat risk awareness",
    "reason_high_temp": "🌡️ High temperature",
    "reason_very_high_temp": "🌡️ Very high temperature",
    "reason_humidity": "💧 High humidity",
    "reason_wind": "🌬️ Low wind speed provides less cooling",
    "reason_none": "✅ No major heat-related weather factor detected.",
    "live_description": "HeatShield AI combines live weather data with machine learning to estimate heat risk and provide practical safety guidance.",
    "enter_description": "Enter a city to retrieve live weather conditions and estimate heat risk using a machine-learning model.",
    "why": "🧠 Why did the AI predict this?",
    "about": "🤖 About the AI",
    "ai_info_1": "HeatShield AI uses a Random Forest machine-learning model trained using weather observations containing temperature, humidity, and wind speed.",
    "ai_info_2": "The system combines the model prediction with a heat-risk score and live weather information to provide an understandable risk assessment.",
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
    "live_description": "يجمع HeatShield AI بيانات الطقس المباشرة مع التعلم الآلي لتقدير مخاطر الحرارة وتقديم إرشادات عملية للسلامة.",
    "enter_description": "أدخل اسم مدينة للحصول على حالة الطقس المباشرة وتقدير مخاطر الحرارة باستخدام نموذج للتعلم الآلي.",
    "why": "🧠 لماذا توقع الذكاء الاصطناعي ذلك؟",
    "about": "🤖 حول الذكاء الاصطناعي",
    "ai_info_1": "يستخدم HeatShield AI نموذج الغابة العشوائية للتعلم الآلي، وقد تم تدريبه باستخدام بيانات الطقس التي تتضمن درجة الحرارة والرطوبة وسرعة الرياح.",
    "ai_info_2": "يجمع النظام بين توقع النموذج ودرجة مخاطر الحرارة وبيانات الطقس المباشرة لتقديم تقييم واضح لمستوى الخطر.",     
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
    "low": "BAJO",
    "moderate": "MODERADO",
    "high": "ALTO",
    "extreme": "EXTREMO",
    "low_advice": "Mantente hidratado y disfruta de tus actividades normales al aire libre.",
    "moderate_advice": "Bebe agua regularmente, descansa a la sombra y evita la exposición prolongada al sol.",
    "high_advice": "Limita las actividades al aire libre, permanece en zonas sombreadas, bebe agua con frecuencia y toma descansos.",
    "extreme_advice": "Evita la exposición prolongada al aire libre y permanece en un lugar fresco o con aire acondicionado.",
    "live_description": "HeatShield AI combina datos meteorológicos en tiempo real con aprendizaje automático para estimar el riesgo de calor y proporcionar recomendaciones prácticas de seguridad.",
    "enter_description": "Introduce una ciudad para obtener las condiciones meteorológicas actuales y estimar el riesgo de calor mediante un modelo de aprendizaje automático.",
    "why": "🧠 ¿Por qué la IA hizo esta predicción?",
    "about": "🤖 Sobre la IA",
    "ai_info_1": "HeatShield AI utiliza un modelo de aprendizaje automático Random Forest entrenado con observaciones meteorológicas que incluyen temperatura, humedad y velocidad del viento.",
    "ai_info_2": "El sistema combina la predicción del modelo con una puntuación de riesgo de calor y datos meteorológicos actuales para proporcionar una evaluación comprensible del riesgo.",
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
    "low": "FAIBLE",
    "moderate": "MODÉRÉ",
    "high": "ÉLEVÉ",
    "extreme": "EXTRÊME",
    "low_advice": "Restez hydraté et profitez normalement de vos activités extérieures.",
    "moderate_advice": "Buvez régulièrement de l'eau, reposez-vous à l'ombre et évitez une exposition prolongée au soleil.",
    "high_advice": "Limitez les activités extérieures, restez à l'ombre, buvez fréquemment et prenez des pauses régulières.",
    "extreme_advice": "Évitez une exposition prolongée à l'extérieur et restez dans un endroit frais ou climatisé.",
    "live_description": "HeatShield AI combine les données météorologiques en temps réel avec l'apprentissage automatique pour estimer le risque de chaleur et fournir des conseils pratiques de sécurité.",
    "enter_description": "Entrez une ville pour obtenir les conditions météorologiques actuelles et estimer le risque de chaleur à l'aide d'un modèle d'apprentissage automatique.",
    "why": "🧠 Pourquoi l'IA a-t-elle fait cette prédiction ?",
    "about": "🤖 À propos de l'IA",
    "ai_info_1": "HeatShield AI utilise un modèle d'apprentissage automatique Random Forest entraîné avec des observations météorologiques comprenant la température, l'humidité et la vitesse du vent.",
    "ai_info_2": "Le système combine la prédiction du modèle avec un score de risque de chaleur et les données météorologiques en temps réel afin de fournir une évaluation compréhensible du risque.",
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
    "low": "कम",
    "moderate": "मध्यम",
    "high": "उच्च",
    "extreme": "अत्यधिक",
    "low_advice": "पानी पीते रहें और सामान्य बाहरी गतिविधियां कर सकते हैं।",
    "moderate_advice": "नियमित रूप से पानी पिएं, छाया में आराम करें और लंबे समय तक सीधी धूप से बचें।",
    "high_advice": "बाहरी गतिविधियों को सीमित करें, छायादार स्थानों में रहें, बार-बार पानी पिएं और नियमित आराम करें।",
    "extreme_advice": "लंबे समय तक बाहर रहने से बचें और ठंडी या वातानुकूलित जगह पर रहें।",
    "live_description": "HeatShield AI गर्मी के जोखिम का अनुमान लगाने और व्यावहारिक सुरक्षा मार्गदर्शन प्रदान करने के लिए लाइव मौसम डेटा को मशीन लर्निंग के साथ जोड़ता है।",
    "enter_description": "मौसम की वर्तमान स्थिति प्राप्त करने और मशीन लर्निंग मॉडल का उपयोग करके गर्मी के जोखिम का अनुमान लगाने के लिए शहर का नाम दर्ज करें।",
    "why": "🧠 AI ने यह अनुमान क्यों लगाया?",
    "about": "🤖 AI के बारे में",
    "ai_info_1": "HeatShield AI एक Random Forest मशीन लर्निंग मॉडल का उपयोग करता है, जिसे तापमान, नमी और हवा की गति वाले मौसम संबंधी डेटा से प्रशिक्षित किया गया है।",
    "ai_info_2": "यह प्रणाली मॉडल के अनुमान को हीट-रिस्क स्कोर और लाइव मौसम डेटा के साथ जोड़कर जोखिम का आसान मूल्यांकन प्रदान करती है।",
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
    "low": "کم",
    "moderate": "درمیانہ",
    "high": "زیادہ",
    "extreme": "انتہائی",
    "low_advice": "پانی پیتے رہیں اور معمول کی بیرونی سرگرمیاں جاری رکھ سکتے ہیں۔",
    "moderate_advice": "باقاعدگی سے پانی پئیں، سایہ میں آرام کریں اور زیادہ دیر تک براہ راست دھوپ سے بچیں۔",
    "high_advice": "بیرونی سرگرمیوں کو محدود کریں، سایہ دار جگہوں پر رہیں، کثرت سے پانی پئیں اور باقاعدہ وقفے لیں۔",
    "extreme_advice": "زیادہ دیر تک باہر رہنے سے گریز کریں اور ٹھنڈی یا ایئر کنڈیشنڈ جگہ پر رہیں۔",
    "live_description": "HeatShield AI گرمی کے خطرے کا اندازہ لگانے اور عملی حفاظتی رہنمائی فراہم کرنے کے لیے براہ راست موسم کے ڈیٹا کو مشین لرننگ کے ساتھ جوڑتا ہے۔",
    "enter_description": "موجودہ موسم کی صورتحال حاصل کرنے اور مشین لرننگ ماڈل کے ذریعے گرمی کے خطرے کا اندازہ لگانے کے لیے شہر کا نام درج کریں۔",
    "why": "🧠 AI نے یہ پیش گوئی کیوں کی؟",
    "about": "🤖 AI کے بارے میں",
    "ai_info_1": "HeatShield AI ایک Random Forest مشین لرننگ ماڈل استعمال کرتا ہے جسے درجہ حرارت، نمی اور ہوا کی رفتار پر مشتمل موسمی مشاہدات سے تربیت دی گئی ہے۔",
    "ai_info_2": "یہ نظام ماڈل کی پیش گوئی کو گرمی کے خطرے کے اسکور اور براہ راست موسم کے ڈیٹا کے ساتھ ملا کر خطرے کا آسان اور قابلِ فہم جائزہ فراہم کرتا ہے۔",
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
    "low": "低",
    "moderate": "中等",
    "high": "高",
    "extreme": "极高",
    "low_advice": "保持充足水分，可以正常进行户外活动。",
    "moderate_advice": "定期喝水，在阴凉处休息，并避免长时间暴露在阳光下。",
    "high_advice": "减少户外活动，尽量待在阴凉处，经常喝水并定期休息。",
    "extreme_advice": "避免长时间在户外活动，并待在凉爽或有空调的环境中。",
    "live_description": "HeatShield AI 将实时天气数据与机器学习相结合，用于评估高温风险并提供实用的安全建议。",
    "enter_description": "输入城市名称以获取实时天气状况，并使用机器学习模型评估高温风险。",
    "why": "🧠 AI 为什么做出这个预测？",
    "about": "🤖 关于 AI",
    "ai_info_1": "HeatShield AI 使用 Random Forest 机器学习模型，该模型使用包含温度、湿度和风速的天气观测数据进行训练。",
    "ai_info_2": "系统将模型预测、高温风险评分和实时天气信息结合起来，为用户提供易于理解的风险评估。",
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

st.markdown(
    f"<h1 style='text-align:center;'>{T['title']}</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h3 style='text-align:center;'>{T['subtitle']}</h3>",
    unsafe_allow_html=True
)

st.markdown(
    f"**{T['description']}**"
)

st.info(
    T["live_description"]
)

st.write(
    T["enter_description"]
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

                st.markdown(
    f"<h2 style='text-align:center;'>📍 {city.strip().title()}</h2>",
    unsafe_allow_html=True
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
                            f"🚨 {T['extreme']} "
                                    f"{T['heat_risk']}\n\n"
                                            f"{T['extreme_advice']}"
                                                )

                elif result["prediction"] == "High":

                                                    st.warning(
                                                            f"⚠️ {T['high']} "
                                                                    f"{T['heat_risk']}\n\n"
                                                                            f"{T['high_advice']}"
                                                                                )

                elif result["prediction"] == "Moderate":

                                                                                    st.warning(
                                                                                            f"🟡 {T['moderate']} "
                                                                                                    f"{T['heat_risk']}\n\n"
                                                                                                            f"{T['moderate_advice']}"
                                                                                                                )

                else:

                                                                                                                    st.success(
                                                                                                                            f"🟢 {T['low']} "
                                                                                                                                    f"{T['heat_risk']}"
                                                                                                                                        )

                # ----------------------------------
                # EXPLANATION
                # ----------------------------------

                st.subheader(T["why"])

                for reason in result["reasons"]:
                    st.write(reason)

                # ----------------------------------
                # RECOMMENDATIONS
                # ----------------------------------

                st.subheader(T["recommendations"])

                advice_key = result["prediction"].lower() + "_advice"

                translated_advice = T.get(
                    advice_key,
                        result["advice"]
                        )

                st.write(translated_advice)

                # ----------------------------------
                # MODEL INFORMATION
                # ----------------------------------

with st.expander(T["about"]):

st.write(T["ai_info_1"])

st.write(T["ai_info_2"])


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "HeatShield AI • AI-powered heat risk awareness"
)
