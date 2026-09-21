import threading
import queue
from gtts import gTTS
import tempfile
import os
import pyttsx3
import uuid

from core.config import is_tts_enabled

# Create a queue to manage TTS tasks
speak_queue = queue.Queue()
stop_flag = False

# Initialize pyttsx3 engine once safely
try:
    fallback_engine = pyttsx3.init()
except Exception as e:
    print(f"⚠️ pyttsx3 initialization warning: {e}")
    fallback_engine = None


def stop_speech():
    """Clear all pending speaking tasks and flag active speech stop."""
    global stop_flag
    stop_flag = True
    while not speak_queue.empty():
        try:
            speak_queue.get_nowait()
            speak_queue.task_done()
        except queue.Empty:
            break
    if fallback_engine:
        try:
            fallback_engine.stop()
        except Exception:
            pass
    print("[STOP] Voice playback stopped.")


def use_pyttsx3(text):
    if not fallback_engine:
        return
    try:
        fallback_engine.say(text)
        fallback_engine.runAndWait()
    except Exception as e:
        print("pyTTSx3 Error:", e)


# TTS speaking function using gTTS and pyttsx3 fallback
def voice_worker():
    global stop_flag
    while True:
        item = speak_queue.get()
        if item is None:
            break  # Stop thread
        
        stop_flag = False
        text, lang = item

        if stop_flag:
            speak_queue.task_done()
            continue

        if lang == "hi":
            try:
                tts = gTTS(text=text, lang="hi")
                filename = os.path.join(tempfile.gettempdir(), f"tts_{uuid.uuid4()}.mp3")
                tts.save(filename)

                if not stop_flag:
                    from playsound import playsound
                    playsound(filename)

                if os.path.exists(filename):
                    os.remove(filename)  # Cleanup
            except Exception as e:
                print("gTTS Failed, trying falling back to pyttsx3. Error:", e)
                if not stop_flag:
                    use_pyttsx3(text)
        else:
            if not stop_flag:
                use_pyttsx3(text)  # Use pyttsx3 for other languages
        
        speak_queue.task_done()


# Start the speaking thread
voice_thread = threading.Thread(target=voice_worker, daemon=True)
voice_thread.start()


# Main speak() function
def speak(text, lang="en"):
    if not is_tts_enabled():
        return  # Don't speak if TTS is off
    
    speak_queue.put((text, lang))  # Add (text, language) tuple to queue
