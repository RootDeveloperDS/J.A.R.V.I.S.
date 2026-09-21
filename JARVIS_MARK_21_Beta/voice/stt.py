'''import speech_recognition as sr
import threading
from core.commands import process_command
from voice.tts import speak
import time

recognizer = sr.Recognizer()
wake_word = "hey jarvis"  # Set your wake word here
wake_word_active = False # Global variable to control wake word mode


# normal talk button usage
def listen_and_respond(output_text):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            output_text.insert("end", "🎤 Listening...\n")
            output_text.see("end")
            audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)
            process_command(command, output_text)

    except Exception as e:
        error_msg = "⚠️ Sorry, I couldn't process that."
        output_text.insert("end", f"{error_msg}\n")
        output_text.see("end")
        print("Error:", e)
        speak(error_msg)

# Thread wrapper
def threaded_listen_and_respond(output_text):
    thread = threading.Thread(target=listen_and_respond, args=(output_text,))
    thread.start()


# 🧠 Wake word mode
wake_word_active = False
def start_wake_word_listener(output_text, mode_flag_func):
    def listen_loop():
        global wake_word_active
        wake_word_active = True
        while wake_word_active:
            if not mode_flag_func():  # Check if wake word mode is on
                time.sleep(1)
                continue

            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("👂 Listening for wake word...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                said = recognizer.recognize_google(audio).lower()
                print("Heard:", said)

                if wake_word in said:
                    speak("Yes SIR?")
                    with sr.Microphone() as source:
                        output_text.insert("end", "🎤 Awaiting your command...\n")
                        output_text.see("end")
                        command_audio = recognizer.listen(source, timeout=5)
                        command = recognizer.recognize_google(command_audio)
                        process_command(command, output_text)

            except Exception as e:
                print("Wake listener error:", e)
                time.sleep(2)

    threading.Thread(target=listen_loop, daemon=True).start()
    
    
def stop_wake_word_listener():
    global wake_word_active
    wake_word_active = False
    print("Wake word listener stopped.")'''
    
    
import speech_recognition as sr
import threading
import time
from core.commands import process_command
from voice.tts import speak, stop_speech
from voice.vad import vad_detector, is_user_speaking
from langdetect import detect,detect_langs, DetectorFactory

DetectorFactory.seed = 0  # For consistent language detection results

recognizer = sr.Recognizer()
wake_word = "jarvis"
wake_word_active = False  # Global toggle for wake word mode


# Function to detect language with strict confidence
import re

# Hindi-like words written in Roman script
HINDI_KEYWORDS = [
    "kaise", "kya", "kyu", "aap", "tum", "hai", "ho", "nahi", "batao", "acha", "theek", "kar", "rakh",
    "mujhe", "tera", "mera", "bhi", "sab", "se", "ab", "main", "hai", "ki", "ka", "ke", "hota", "hona",
    "chalo", "karo", "karna", "jarurat", "kyunki", "kyon", "tumhara", "mera", "acha", "sahi"
]

def detect_language_smart(text):
    text = text.lower()
    
    # Match Roman Hindi words
    hindi_score = sum(1 for word in HINDI_KEYWORDS if word in text)

    # Also check langdetect confidence
    try:
        langs = detect_langs(text)
        if langs[0].lang == "hi" and langs[0].prob > 0.5:
            return "hi"
    except:
        pass

    # If Hindi keywords appear more than 1 time, treat as Hindi
    if hindi_score >= 2:
        return "hi"

    return "en"



# 🔊 Normal talk button usage with language detection
def listen_and_respond(output_text):
    try:
        stop_speech()  # Interrupt any ongoing assistant speech
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            output_text.insert("end", "🎤 Listening...\n")
            output_text.see("end")
            audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)
            
            #detect language
            print(f"🎤 Heard: {command}")
            
            #language = detect(command)
            language = detect_language_smart(command)
            print(f"🔍 Detected Language: {language}")

            # Process based on detected language
            process_command(command, output_text, language)

    except Exception as e:
        error_msg = "⚠️ Sorry, I couldn't process that."
        output_text.insert("end", f"{error_msg}\n")
        output_text.see("end")
        print("Error:", e)
        speak(error_msg, lang='en')

# Threaded wrapper for Normal Mode
def threaded_listen_and_respond(output_text):
    thread = threading.Thread(target=listen_and_respond, args=(output_text,))
    thread.start()

# 🧠 Wake Word Mode
def start_wake_word_listener(output_text, mode_flag_func):
    def listen_loop():
        global wake_word_active
        wake_word_active = True

        while wake_word_active:
            if not mode_flag_func():
                time.sleep(1)
                continue

            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("👂Listening for wake word...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                said = recognizer.recognize_google(audio).lower()
                print("Heard:", said)

                if wake_word in said:
                    speak("Yes SIR?", lang='en')
                    with sr.Microphone() as source:
                        output_text.insert("end", "🎤 Awaiting your command...\n")
                        output_text.see("end")
                        command_audio = recognizer.listen(source, timeout=5)
                        command = recognizer.recognize_google(command_audio)
                        language = detect(command)
                        print(f"🔍 Detected Language: {language}")
                        process_command(command, output_text, language)

            except Exception as e:
                print("Wake listener error:", e)
                time.sleep(2)

    threading.Thread(target=listen_loop, daemon=True).start()

def stop_wake_word_listener():
    global wake_word_active
    wake_word_active = False
    print("🛑 Wake word listener stopped.")