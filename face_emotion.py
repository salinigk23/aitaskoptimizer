import cv2
from deepface import DeepFace

def detect_facial_emotion():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None, "❌ Webcam not accessible."
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None, "❌ Failed to capture image."
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = analysis[0]['dominant_emotion'].lower()
        return emotion, None
    except Exception as e:
        return None, str(e)