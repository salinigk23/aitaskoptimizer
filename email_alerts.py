import smtplib
from email.message import EmailMessage

HR_EMAIL = "hr@example.com"
FROM_EMAIL = "yourcompany.bot@example.com"
APP_PASSWORD = "your-app-password"

def send_alert(user_text, detected_emotion):
    msg = EmailMessage()
    msg["Subject"] = f"⚠️ Emotion Alert: {detected_emotion.capitalize()} Detected"
    msg["From"] = FROM_EMAIL
    msg["To"] = HR_EMAIL
    msg.set_content(f"""
Detected Emotion: {detected_emotion}
User Message: {user_text}
Action: Please consider checking in with this employee.
""")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(FROM_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print("Email error:", e)