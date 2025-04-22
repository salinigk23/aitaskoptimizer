def get_task_recommendations(emotion):
    task_map = {
        "joy": ["Collaborate on creative projects", "Lead a meeting", "Help a colleague"],
        "sadness": ["Do low-pressure solo work", "Take a short break", "Write in your journal"],
        "anger": ["Avoid meetings", "Do independent work", "Take a walk"],
        "fear": ["Start with a small task", "Use a checklist", "Do guided breathing"],
        "neutral": ["Plan your day", "Organize your inbox", "Do routine work"],
        "surprise": ["Capture ideas quickly", "Explore something new"],
        "disgust": ["Switch tasks temporarily", "Step away for a break"]
    }
    return task_map.get(emotion.lower(), ["No recommendations available."])