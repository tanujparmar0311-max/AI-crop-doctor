import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pyttsx3

# 🎯 Page config
st.set_page_config(page_title="AI Crop Doctor 🌿", layout="centered")

# 🎨 Styling
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.result-box {
    padding:20px;
    border-radius:15px;
    background:#1e293b;
    box-shadow:0 0 15px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# 🎯 Load model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.keras")

model = load_model()

# 🎯 Classes
class_names = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus', 'Tomato_healthy'
]

# 💊 Solutions
solutions_dict = {
    "Tomato Early Blight": "Remove infected leaves immediately, apply fungicides like chlorothalonil or mancozeb every 7–10 days, and ensure proper spacing between plants.",

    "Tomato Late Blight": "Remove and destroy infected plants immediately, apply systemic fungicides such as metalaxyl, and avoid overhead irrigation to prevent spread.",

    "Tomato Leaf Mold": "Improve air circulation, reduce humidity levels, avoid overcrowding, and apply appropriate fungicides if infection increases.",

    "Tomato Septoria Leaf Spot": "Remove affected leaves, apply fungicides regularly, mulch around plants to prevent soil splash, and water at the base.",

    "Tomato Spider Mites Two Spotted Spider Mite": "Spray neem oil or insecticidal soap on leaves, increase humidity, and regularly wash plants with water to remove mites.",

    "Tomato Target Spot": "Apply fungicides like azoxystrobin or mancozeb, remove infected leaves, and maintain proper plant spacing.",

    "Tomato Yellowleaf Curl Virus": "Control whiteflies using insecticides or sticky traps, remove infected plants immediately, and use resistant crop varieties.",

    "Tomato Mosaic Virus": "Remove infected plants, disinfect tools and hands, and avoid handling plants after tobacco use to prevent spread.",

    "Potato Early Blight": "Apply fungicides, remove infected foliage, practice crop rotation, and maintain proper plant nutrition.",

    "Potato Late Blight": "Use systemic fungicides immediately, destroy infected plants, and avoid wet conditions around plants.",

    "Pepper Bell Bacterial Spot": "Apply copper-based bactericides, avoid overhead watering, remove infected leaves, and ensure proper spacing for airflow.",

    "Healthy": "🌿 Your plant is healthy and well-maintained! Keep providing proper sunlight, watering, and nutrients to maintain its excellent condition."
}
# 📘 Explanation
explanations = {
     "Tomato Early Blight": "A common fungal disease caused by Alternaria solani. It appears as dark brown spots with concentric rings on older leaves. It spreads in warm and humid conditions and can reduce yield significantly if not controlled.",

    "Tomato Late Blight": "A serious and fast-spreading disease caused by Phytophthora infestans. It leads to large dark lesions on leaves and stems. It thrives in cool, wet conditions and can destroy entire crops rapidly.",

    "Tomato Leaf Mold": "A fungal disease caused by Passalora fulva, mainly affecting greenhouse tomatoes. It appears as yellow spots on upper leaf surfaces and mold growth underneath. High humidity accelerates its spread.",

    "Tomato Septoria Leaf Spot": "Caused by Septoria lycopersici, this disease creates small circular spots with dark borders. It usually starts on lower leaves and spreads upward, especially in wet conditions.",

    "Tomato Spider Mites Two Spotted Spider Mite": "A pest infestation rather than a disease. These tiny mites suck plant sap, causing yellow speckling and leaf damage. They thrive in hot and dry environments.",

    "Tomato Target Spot": "A fungal disease that produces circular brown lesions with concentric rings. It affects leaves, stems, and fruits, reducing overall plant health and yield.",

    "Tomato Yellowleaf Curl Virus": "A viral disease transmitted by whiteflies. It causes leaf curling, yellowing, and stunted growth. Infected plants produce very low yield and cannot be cured.",

    "Tomato Mosaic Virus": "A viral infection that causes mottled light and dark green patterns on leaves. It spreads through contaminated tools and handling and reduces plant productivity.",

    "Potato Early Blight": "A fungal disease that produces dark spots with concentric rings on leaves. It affects older foliage first and reduces photosynthesis and yield.",

    "Potato Late Blight": "A highly destructive disease caused by Phytophthora infestans. It leads to rapid decay of leaves and tubers, especially in cool and moist climates.",

    "Pepper Bell Bacterial Spot": "A bacterial infection that causes small, water-soaked lesions on leaves and fruits. It spreads through rain and irrigation and can significantly damage crops.",

    "Healthy": "The plant shows no visible signs of disease or stress. It indicates proper care, balanced nutrition, and a suitable growing environment. Maintaining these conditions will ensure continued healthy growth."
}

# 🔊 Better voice
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# 🔧 Clean class name
def clean_name(name):
    name = name.replace("___", " ").replace("__", " ")
    name = name.replace("_", " ")
    return name.strip().title()

# 🌿 Title
st.title("🌿 AI Crop Doctor")
st.write("Upload a leaf image → Detect disease → Get solution")

# 📤 Upload only
uploaded_file = st.file_uploader("📷 Upload Leaf Image", type=["jpg","png","jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    img = Image.open(uploaded_file).convert("RGB")

    with col1:
        st.image(img, caption="Leaf Image", use_column_width=True)

    # preprocess
    img_resized = img.resize((224,224))
    img_array = np.array(img_resized)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    with st.spinner("🧠 AI is analyzing..."):
        prediction = model.predict(img_array)
        class_index = np.argmax(prediction)
        confidence = np.max(prediction)

    raw_class = class_names[class_index]
    predicted_class = clean_name(raw_class)

    if "healthy" in raw_class.lower():
        predicted_class = "Healthy"
        solution = solutions_dict["Healthy"]
        explanation = "No disease detected. The plant is in excellent condition."
    else:
        solution = solutions_dict.get(predicted_class, "Consult an agricultural expert for proper diagnosis.")
        explanation = explanations.get(predicted_class, "No detailed explanation available.")
    explanation = explanations.get(predicted_class, "No explanation available")

    with col2:
        st.markdown(f"""
        <div class="result-box">
        <h3>🧠 Disease</h3>
        <p><b>{predicted_class}</b></p>

        <h3>📊 Confidence</h3>
        <p>{confidence:.2%}</p>

        <h3>📘 Explanation</h3>
        <p>{explanation}</p>

        <h3>💊 Solution</h3>
        <p>{solution}</p>
        </div>
        """, unsafe_allow_html=True)

    # 🔊 Speak button
    if st.button("🔊 Speak Result"):
        if "healthy" in raw_class.lower():
            predicted_class = "Healthy"
            solution = solutions_dict["Healthy"]
            explanation = "No disease detected. The plant is in excellent condition."
        else:
            solution = solutions_dict.get(predicted_class, "Consult an agricultural expert for proper diagnosis.")
            explanation = explanations.get(predicted_class, "No detailed explanation available.")