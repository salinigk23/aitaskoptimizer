import streamlit as st
from transformers import pipeline
import speech_recognition as sr
from emotion_logger import init_db, log_emotion
from face_emotion import detect_facial_emotion
from email_alerts import send_alert
from task_recommender import get_task_recommendations

# Load model once
@st.cache_resource
def load_emotion_model():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_classifier = load_emotion_model()
init_db()

alert_emotions = ["sadness", "anger", "fear", "disgust"]

st.set_page_config(page_title="Emotion Task Recommender", layout="centered")
st.title("🧠 Emotion-Aware Task Recommender")

st.sidebar.markdown("## 👤 Your Info")
user_id = st.sidebar.text_input("Enter your name or ID")
consent = st.sidebar.checkbox("✅ I consent to emotion logging and task suggestions")
if not consent:
    st.warning("You must provide consent to use this app.")
    st.stop()

import hashlib
def anonymize_name(name):
    return hashlib.sha256(name.encode()).hexdigest()

user_id = anonymize_name(user_id) if user_id else None

st.write("Choose your input method to detect your mood and get task suggestions.")
input_mode = st.radio("Input Mode:", ["💬 Text", "🎙️ Voice", "📸 Webcam"])

user_input = None
emotion = None
confidence = None
analyze = False

if input_mode == "💬 Text":
    user_input = st.text_area("Describe how you feel:")
    analyze = st.button("Analyze")
elif input_mode == "🎙️ Voice":
    if st.button("🎤 Speak Now"):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            st.info("🎙️ Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            st.write(f"📝 You said: `{user_input}`")
            analyze = True
        except:
            st.error("❌ Could not understand voice input.")
elif input_mode == "📸 Webcam":
    if st.button("📸 Analyze Facial Expression"):
        with st.spinner("Analyzing facial emotion..."):
            emotion, error = detect_facial_emotion()
        if emotion:
            st.success(f"**Detected Emotion:** {emotion.capitalize()}")
            analyze = True
        else:
            st.error(error)

if analyze:
    if input_mode != "📸 Webcam":
        with st.spinner("Detecting emotion..."):
            result = emotion_classifier(user_input)[0]
            emotion = result['label'].lower()
            confidence = result['score']
            st.success(f"**Detected Emotion:** {emotion.capitalize()} (Confidence: {confidence:.2f})")
    
    tasks = get_task_recommendations(emotion)
    st.markdown("### ✅ Recommended Tasks:")
    for task in tasks:
        st.markdown(f"- {task}")

    if user_id:
        log_emotion(user_id, input_mode[2:], user_input, emotion, confidence, tasks)
    else:
        st.warning("Please enter your name to save the log.")

    if emotion in alert_emotions:
        send_alert(user_input or "From webcam", emotion)