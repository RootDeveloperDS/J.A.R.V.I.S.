import os
import json
from datetime import datetime, timedelta
try:
    import dateparser
except ImportError:
    dateparser = None

REMINDERS_FILE = os.path.join("DATA", "reminders.json")
os.makedirs("DATA", exist_ok=True)

#load existing reminders from JSON
def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    try:
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

# Save reminders to file
def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

# add a new reminder
def add_reminder(text, delay_minutes):
    reminders = load_reminders()
    remind_time = (datetime.now() + timedelta(minutes=delay_minutes)).strftime("%Y-%m-%d %H:%M:%S")
    reminders.append({"text": text, "time": remind_time})
    save_reminders(reminders)

def add_natural_reminder(text): #new function to add reminders using natural language
    if not dateparser:
        return False, "dateparser library not installed."
    reminder = {
        "task": None,
        "time": None
    }

    parsed_time = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})
    if parsed_time:
        reminder["time"] = parsed_time.strftime("%Y-%m-%d %H:%M:%S")

        # Try to guess task by removing the time expression
        task = text.split("to", 1)[-1].strip() if "to" in text else text
        reminder["task"] = task

        reminders = load_reminders()
        reminders.append(reminder)
        save_reminders(reminders)
        return True, f"Reminder saved: {task} at {parsed_time.strftime('%Y-%m-%d %I:%M %p')}"
    
    return False, "Sorry, I couldn’t understand the time you mentioned."



import time
from voice.tts import speak

def start_reminder_checker(output_text):
    def check_reminders_loop():
        while True:
            reminders = load_reminders()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_reminders = []

            for reminder in reminders:
                if reminder["time"] <= now:
                    #message = f"⏰ Reminder: {reminder['text']}"
                    task_text = reminder.get("task") or reminder.get("text") or "Unknown task"
                    message = f"⏰ Reminder: {task_text}"
                    output_text.insert("end", message + "\n")
                    output_text.see("end")
                    speak(message)
                else:
                    new_reminders.append(reminder)

            save_reminders(new_reminders)
            time.sleep(20)  # check every 20 seconds
    import threading
    threading.Thread(target=check_reminders_loop, daemon=True).start()
