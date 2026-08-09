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
    "intro": "أدخل اسم مدينة للحصول على حالة الطقس الحالية وتقدير مخاطر الحرارة باستخدام نموذج للتعلم الآلي.",
    "spinner": "جارٍ الحصول على الطقس وتحليل المخاطر...",
    "empty_city": "يرجى إدخال اسم المدينة.",
    "alert_low": "🟢 خطر حرارة منخفض",
    "alert_moderate": "🟡 خطر حرارة متوسط",
    "alert_high": "🟠 خطر حرارة مرتفع",
    "alert_extreme": "🚨 تحذير من حرارة شديدة",
    "about_text": "يستخدم HeatShield AI نموذج Random Forest للتعلم الآلي، تم تدريبه باستخدام بيانات الطقس التي تشمل درجة الحرارة والرطوبة وسرعة الرياح.",
    "about_text2": "يجمع النظام بين توقع النموذج ودرجة مخاطر الحرارة وبيانات الطقس المباشرة لتقديم تقييم واضح للمخاطر.",
    "footer": "HeatShield AI • التوعية بمخاطر الحرارة باستخدام الذكاء الاصطناعي",
    "reason_high_temp": "🌡️ درجة حرارة مرتفعة",
    "reason_very_high_temp": "🌡️ درجة حرارة مرتفعة جدًا",
    "reason_humidity": "💧 رطوبة مرتفعة",
    "reason_wind": "🌬️ انخفاض سرعة الرياح يوفر تبريدًا أقل",
    "reason_none": "✅ لم يتم اكتشاف عامل رئيسي متعلق بالحرارة.",
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
    "intro": "Introduce una ciudad para obtener las condiciones meteorológicas actuales y estimar el riesgo de calor mediante aprendizaje automático.",
    "spinner": "Obteniendo el clima actual y analizando el riesgo...",
    "empty_city": "Introduce el nombre de una ciudad.",
    "alert_low": "🟢 BAJO RIESGO DE CALOR",
    "alert_moderate": "🟡 RIESGO MODERADO DE CALOR",
    "alert_high": "⚠️ ALTO RIESGO DE CALOR",
    "alert_extreme": "🚨 ALERTA DE CALOR EXTREMO",
    "about_text": "HeatShield AI utiliza un modelo de aprendizaje automático Random Forest entrenado con observaciones meteorológicas que incluyen temperatura, humedad y velocidad del viento.",
    "about_text2": "El sistema combina la predicción del modelo con una puntuación de riesgo térmico y datos meteorológicos en directo para ofrecer una evaluación comprensible.",
    "footer": "HeatShield AI • Concienciación sobre el riesgo de calor mediante IA",
    "reason_high_temp": "🌡️ Temperatura alta",
    "reason_very_high_temp": "🌡️ Temperatura muy alta",
    "reason_humidity": "💧 Humedad alta",
    "reason_wind": "🌬️ La baja velocidad del viento proporciona menos refrigeración",
    "reason_none": "✅ No se detectó ningún factor meteorológico importante relacionado con el calor.",
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
    "intro": "Entrez une ville pour obtenir les conditions météorologiques actuelles et estimer le risque de chaleur grâce à l'apprentissage automatique.",
    "spinner": "Récupération de la météo et analyse du risque...",
    "empty_city": "Veuillez entrer le nom d'une ville.",
    "alert_low": "🟢 FAIBLE RISQUE DE CHALEUR",
    "alert_moderate": "🟡 RISQUE DE CHALEUR MODÉRÉ",
    "alert_high": "⚠️ RISQUE DE CHALEUR ÉLEVÉ",
    "alert_extreme": "🚨 ALERTE DE CHALEUR EXTRÊME",
    "about_text": "HeatShield AI utilise un modèle d'apprentissage automatique Random Forest entraîné avec des observations météorologiques comprenant la température, l'humidité et la vitesse du vent.",
    "about_text2": "Le système combine la prédiction du modèle avec un score de risque thermique et des données météorologiques en direct pour fournir une évaluation compréhensible.",
    "footer": "HeatShield AI • Sensibilisation aux risques liés à la chaleur grâce à l'IA",
    "reason_high_temp": "🌡️ Température élevée",
    "reason_very_high_temp": "🌡️ Température très élevée",
    "reason_humidity": "💧 Humidité élevée",
    "reason_wind": "🌬️ La faible vitesse du vent offre moins de refroidissement",
    "reason_none": "✅ Aucun facteur météorologique majeur lié à la chaleur n'a été détecté.",
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
    "intro": "लाइव मौसम की जानकारी प्राप्त करने और मशीन-लर्निंग मॉडल से गर्मी के जोखिम का अनुमान लगाने के लिए शहर दर्ज करें।",
    "spinner": "लाइव मौसम प्राप्त किया जा रहा है और जोखिम का विश्लेषण हो रहा है...",
    "empty_city": "कृपया शहर का नाम दर्ज करें।",
    "alert_low": "🟢 गर्मी का कम जोखिम",
    "alert_moderate": "🟡 गर्मी का मध्यम जोखिम",
    "alert_high": "⚠️ गर्मी का उच्च जोखिम",
    "alert_extreme": "🚨 अत्यधिक गर्मी की चेतावनी",
    "about_text": "HeatShield AI एक Random Forest मशीन-लर्निंग मॉडल का उपयोग करता है, जिसे तापमान, नमी और हवा की गति वाले मौसम डेटा पर प्रशिक्षित किया गया है।",
    "about_text2": "यह सिस्टम मॉडल की भविष्यवाणी, हीट-रिस्क स्कोर और लाइव मौसम की जानकारी को मिलाकर जोखिम का आसान आकलन देता है।",
    "footer": "HeatShield AI • AI द्वारा गर्मी के जोखिम के प्रति जागरूकता",
    "reason_high_temp": "🌡️ अधिक तापमान",
    "reason_very_high_temp": "🌡️ बहुत अधिक तापमान",
    "reason_humidity": "💧 अधिक नमी",
    "reason_wind": "🌬️ कम हवा की गति से ठंडक कम मिलती है",
    "reason_none": "✅ गर्मी से संबंधित कोई प्रमुख मौसम कारक नहीं मिला।",
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
    "intro": "لائیو موسم کی صورتحال حاصل کرنے اور مشین لرننگ ماڈل کے ذریعے گرمی کے خطرے کا اندازہ لگانے کے لیے شہر درج کریں۔",
    "spinner": "لائیو موسم حاصل کیا جا رہا ہے اور خطرے کا تجزیہ ہو رہا ہے...",
    "empty_city": "براہ کرم شہر کا نام درج کریں۔",
    "alert_low": "🟢 گرمی کا کم خطرہ",
    "alert_moderate": "🟡 گرمی کا درمیانہ خطرہ",
    "alert_high": "⚠️ گرمی کا زیادہ خطرہ",
    "alert_extreme": "🚨 شدید گرمی کا انتباہ",
    "about_text": "HeatShield AI ایک Random Forest مشین لرننگ ماڈل استعمال کرتا ہے جسے درجہ حرارت، نمی اور ہوا کی رفتار کے موسمی ڈیٹا پر تربیت دی گئی ہے۔",
    "about_text2": "یہ نظام ماڈل کی پیش گوئی، ہیٹ رسک اسکور اور لائیو موسم کی معلومات کو ملا کر خطرے کا آسان جائزہ فراہم کرتا ہے۔",
    "footer": "HeatShield AI • AI کے ذریعے گرمی کے خطرے سے آگاہی",
    "reason_high_temp": "🌡️ زیادہ درجہ حرارت",
    "reason_very_high_temp": "🌡️ بہت زیادہ درجہ حرارت",
    "reason_humidity": "💧 زیادہ نمی",
    "reason_wind": "🌬️ ہوا کی کم رفتار سے ٹھنڈک کم ملتی ہے",
    "reason_none": "✅ گرمی سے متعلق کوئی اہم موسمی عنصر نہیں ملا۔",
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
    "intro": "输入城市以获取实时天气状况，并使用机器学习模型估算高温风险。",
    "spinner": "正在获取实时天气并分析风险...",
    "empty_city": "请输入城市名称。",
    "alert_low": "🟢 低热风险",
    "alert_moderate": "🟡 中等热风险",
    "alert_high": "⚠️ 高热风险",
    "alert_extreme": "🚨 极端高温警报",
    "about_text": "HeatShield AI 使用 Random Forest 机器学习模型，该模型使用包含温度、湿度和风速的天气数据进行训练。",
    "about_text2": "系统将模型预测、热风险评分和实时天气信息结合起来，为用户提供易于理解的风险评估。",
    "footer": "HeatShield AI • AI 驱动的高温风险预警",
    "reason_high_temp": "🌡️ 高温",
    "reason_very_high_temp": "🌡️ 极高温度",
    "reason_humidity": "💧 高湿度",
    "reason_wind": "🌬️ 风速较低，降温效果较弱",
    "reason_none": "✅ 未检测到明显的高温相关天气因素。",
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
        reasons.append(T["reason_very_high_temp"])

    elif temp >= 38:
        reasons.append(T["reason_high_temp"])

    if humidity >= 70:
        reasons.append(T["reason_humidity"])

    if wind_ms <= 5:
        reasons.append(T["reason_wind"])

    if not reasons:
        reasons.append(T["reason_none"])

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

st.write(T["intro"])

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

        st.warning(T["empty_city"])

    else:

        with st.spinner(T["spinner"]):

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

                translated_risk = T.get(
                    result["prediction"].lower(),
                    result["risk_name"]
                )

                st.markdown(
                    f"## {result['emoji']} {translated_risk}"
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
                        f"{T['alert_extreme']}\n\n"
                        f"{T['extreme_advice']}"
                    )

                elif result["prediction"] == "High":

                    st.warning(
                        f"{T['alert_high']}\n\n"
                        f"{T['high_advice']}"
                    )

                elif result["prediction"] == "Moderate":

                    st.warning(
                        f"{T['alert_moderate']}\n\n"
                        f"{T['moderate_advice']}"
                    )

                else:

                    st.success(
                        T["alert_low"]
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

                    st.write(
                        T["about_text"]
                    )

                    st.write(
                        T["about_text2"]
                    )


# ==========================================
# FOOTER
# ========================================== 

st.divider()

st.caption(
    T["footer"]
)
