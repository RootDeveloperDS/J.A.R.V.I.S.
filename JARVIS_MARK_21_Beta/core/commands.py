import os ,threading
import webbrowser
from datetime import datetime, timedelta
import json
import tkinter as tk
#import subprocess
from features.notes import add_note, delete_note, load_notes
from features.reminders import add_reminder, load_reminders, save_reminders
from features.music import load_music_from, play_music, pause_music, resume_music, stop_music, next_song, shuffle_music
from voice.tts import speak
from api.gemini import model
from core.memory import conversation_history, remember, recall,load_memory
from core.utils import type_and_speak_text,start_spinner, stop_spinner, update_spinner
import string
from features.reminders import add_reminder, add_natural_reminder
from urllib.parse import quote_plus
import psutil
import re
from pycaw.pycaw import AudioUtilities

from core.plugin_loader import load_plugins
plugin_registry = load_plugins()#to load all plugin triggers 

for k in plugin_registry:# for debugging purposes
    print(f"✅ Plugin loaded: {k}")


# define Path to chat log
CHAT_LOG_FILE = os.path.join("DATA", "chat_log.txt")

UNKNOWN_FILE = os.path.join("DATA", "unknown_commands.txt")
CUSTOM_FILE = os.path.join("DATA", "custom_commands.json")

import subprocess
import webbrowser
import os
'''
def execute_learned_action(action):
    actions = action.split(" and ")
    for a in actions:
        a = a.strip()
        try:
            if a.startswith("open "):
                a = a.replace("open ", "", 1).strip()

            if a.startswith("http") or ".com" in a:
                webbrowser.open(a)
            elif ".exe" in a or os.path.exists(a):
                os.startfile(a)
            else:
                subprocess.Popen(a, shell=True)

        except Exception as e:
            print(f"⚠️ Failed to run: {a} -> {e}")'''















def process_command(command, output_text,language="en"):
    handled_by_gemini= False  # Flag to check if command is handled by Gemini
    command = command.lower()

    # Add user command to conversation history
    conversation_history.append({"user": command, "jarvis": ""})
    # Limit memory to last 20
    
    
    if len(conversation_history) > 20:
        conversation_history[:] = conversation_history[-20:]

    # Create context(last 5 interactions)
    context = ""
    for chat in conversation_history[-5:]:  #limit context to last 5 exchanges
        context += f"User: {chat['user']}\nJarvis: {chat['jarvis']}\n"
    #Build Full Prompt
    full_prompt = context + f"User: {command}\nJarvis:"
    #Display user command to GUI
    output_text.insert("end", f"🗣 You said: {command}\n")
    output_text.see("end")
    output_text.update()  # Ensure GUI updates immediately

    # Check if user command matches or handled by a plugin 
    for trigger, plugin in plugin_registry.items():
        #if trigger in command.lower():
        if trigger in command:
            plugin["run"](command, output_text)
            return  # Stop after running plugin
    # If no plugin handled it, continue with known commands and Gemini response

    def lasttasks(command, reply, output_text, language):
        # 1. Save reply/conversation history in memory
        conversation_history[-1]["jarvis"] = reply

        # 2. Add new conversation to log file
        with open(CHAT_LOG_FILE, "a", encoding="utf-8") as file:
            file.write(f"You: {command}\nJarvis: {reply}\n\n")

        # 3. Display reply in GUI
        type_and_speak_text(output_text, reply,language=language)  # types and speaks the reply in GUI



    # Load custom commands
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r") as f:
            custom_commands = json.load(f)
    else:
        custom_commands = {}

    # Check if this is a learned command
    '''for trigger in custom_commands:
        if trigger.lower() in command:
            action = custom_commands[trigger]
            execute_learned_action(action)
            reply = f"🧠 Executing your custom command: {action}"
            output_text.insert("end", f"🤖 Jarvis: {reply}\n")
            speak(reply)
            return'''
       
    
    # Check if this is a learned command
    for trigger, action in custom_commands.items():
        if trigger.lower() in command:
            reply = f"Executing command"#{action}"
            output_text.insert("end", f"🤖 Jarvis: {reply}\n")
            output_text.update()  # Ensure GUI updates immediately
            speak(reply)

            # Split multiple actions by "and"
            actions = [a.strip() for a in action.split("and")]

            for act in actions:
               if act.startswith("open "):
                    target = act.replace("open", "").strip()

                    # Open apps (based on path or known app name)
                    try:
                        if target.startswith("http"):
                            webbrowser.open(target)
                        elif ".exe" in target or os.path.exists(target):
                            os.startfile(target)
                        else:
                            subprocess.Popen(["start", "", target], shell=True)
                    except Exception as e:
                        print(f"⚠️ Failed to open {target}: {e}")
            return

    
     
    # If no custom command matched, continue with known commands or Gemini response



    # Process Known Commands

    if "search google for" in command:
            query = command.split("search google for", 1)[1].strip()

            if query:
                reply = f"Searching Google for {query}..."
                webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
            else:
                reply = "Please tell me what you would like to search on Google"
    
    elif "search youtube for" in command:
            query = command.split("search youtube for", 1)[1].strip()

            if query:
                reply = f"Searching YouTube for {query}..."
                webbrowser.open(f"https://www.youtube.com/results?search_query={quote_plus(query)}")
            else:
                reply = "Please tell me what you would like to search on YouTube"

    elif "open youtube" in command:
        reply = "Opening YouTube..."
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        reply = "Opening Google..."
        webbrowser.open("https://www.google.com")

    elif "stop" in command or "exit" in command:
        with open(CHAT_LOG_FILE, "w", encoding="utf-8") as file:
            for item in conversation_history:
                file.write(f"You: {item['user']}\nJarvis: {item['jarvis']}\n\n")
        reply = "Goodbye!"
        output_text.insert("end", f"🤖 Jarvis: {reply}\n")
        output_text.update()  # Ensure GUI updates immediately
        speak(reply)
        exit()

    elif "play music" in command:
        reply = "Playing your music!" if load_music_from() else "No songs found in your music folder."
        play_music()

    elif "next song" in command:
        next_song()
        reply = "Skipping to the next song."

    elif "pause music" in command:
        pause_music()
        reply = "Music paused."

    elif "resume music" in command:
        resume_music()
        reply = "Resuming music."

    elif "stop music" in command:
        stop_music()
        reply = "Music stopped."

    elif "shuffle music" in command:
        shuffle_music()
        reply = "Shuffling and playing music."

    elif "show chat history" in command:
        if conversation_history:
            reply = "\n".join([f"You: {item['user']}\nJarvis: {item['jarvis']}" for item in conversation_history])
        else:
            reply = "No chat history yet."

    elif "save chat" in command:
        with open(CHAT_LOG_FILE, "w", encoding="utf-8") as file:
            for item in conversation_history:
                file.write(f"You: {item['user']}\nJarvis: {item['jarvis']}\n\n")
        reply = "Chat history saved to chat_log.txt."

    elif "add note" in command or "remember this note" in command:
        note = command.replace("add note", "").replace("remember this note", "").strip()
        reply = f"Note added: {note}" if note else "What would you like me to note down?"
        if note:
            add_note(note)

    elif "show notes" in command or "view notes" in command:
        notes = load_notes()
        reply = "Here are your notes:\n" + "\n".join([f"- {n}" for n in notes]) if notes else "No notes found."

    elif "delete note" in command or "remove note" in command:
        note = command.replace("delete note", "").replace("remove note", "").strip()
        reply = f"Deleted note: {note}" if delete_note(note) else "Couldn't find that note to delete."

        '''elif "remind me to" in command and "in" in command:#reminder handling
        try:
            parts = command.split("remind me to")[1].strip()
            task, time_part = parts.rsplit(" in ", 1)
            delay = int(''.join(filter(str.isdigit, time_part)))    #extract numbers
            add_reminder(task, delay)
            reply = f"Okay, I'll remind you to {task} in {delay} minute(s)."
        except Exception:
            reply = "Sorry, I couldn't understand the reminder format."
            '''
    
    elif "remind me to" in command.lower():
        try:
            if " in " in command.lower():
                # Time delay style: remind me to take medicine in 15 minutes
                parts = command.lower().split("remind me to")[1].strip()
                task, time_part = parts.rsplit(" in ", 1)
                delay = int(''.join(filter(str.isdigit, time_part)))  # extract minutes
                add_reminder(task.strip(), delay)
                reply = f"Okay✅ Reminder set: I'll remind you to **{task.strip()}** in **{delay} minute(s)**."
        
            else:
                # Natural language style: remind me to call mom tomorrow at 5PM
                success, msg = add_natural_reminder(command)
                reply = msg if success else "Sorry, I couldn't understand the reminder format."

        except Exception as e:
            reply = "⚠️ Reminder format error. Try saying: remind me to walk in 5 minutes."

    
    
    elif "view reminders" in command or "show reminders" in command or "list reminders" in command:# view reminders
        reminders = load_reminders()
        if not reminders:
            reply = "You have no reminders set."
        else:
            reply = "Here are your reminders:\n" + "\n".join([f"- {rem['text']} at {rem['time']}" for rem in reminders])

    elif "remember that my" in command.lower() or "remember that" in command.lower():
        # Example: remember that my college is GGITS
        parts = command.lower().split("remember that")
        if len(parts) > 1:
            memory_phrase = parts[1].strip()
            if " is " in memory_phrase:
                key, value = memory_phrase.split(" is ", 1)
                remember(key.strip(), value.strip())
                reply = f"Got it! I’ll remember that your {key.strip()} is {value.strip()}."
            else:
                reply = "Please say it like: remember that my birthday is October 5th."
        
        
        
        ''' elif "what is my" in command.lower() or "do you remember" in command.lower() or "what do you remember" in command.lower() or "what did i tell you" in command.lower():
        # Example: what is my name / do you remember my name
        # Example: what is my birthday / do you remember my college
        key = command.replace("what is my", "").replace("do you remember", "").strip()
        value = recall(key)
        reply = f"You told me your {key} is {value}."   '''


        
        '''elif any(phrase in command.lower() for phrase in ["what is my", "do you remember", "what did i tell you", "what do you remember"]):
        import string  # for punctuation cleaning 
        # Clean input
        lowered = command.lower().strip()

        # Remove trigger phrases
        for phrase in ["what is my", "do you remember", "what do you remember", "what did i tell you"]:
            lowered = lowered.replace(phrase, "")

        # Remove punctuation and extra spaces
        key = lowered.translate(str.maketrans('', '', string.punctuation)).strip()

        if key:
            value = recall(key)
            reply = f"You told me your {key} is {value}."
        else:
            reply = "Please ask me something specific you told me earlier."
'''

    elif any (phrase in command.lower() for phrase in ["what is my", "do you remember", "what do you remember", "what did i tell you"]):
        lowered = command.lower().strip()

        # Detect if user said just: "what do you remember"
        if lowered in ["what do you remember", "what did i tell you"]:
            memory = load_memory()
            if memory:
                reply = "Here’s what I remember:\n" + "\n".join([f"🧠 {k}: {v}" for k, v in memory.items()])
            else:
                reply = "I don't remember anything yet."
            #return type_and_speak_text(output_text, reply)

        # Otherwise, extract key normally
        for phrase in ["what is my", "do you remember", "what did i tell you", "what do you remember"]:
            lowered = lowered.replace(phrase, "")

        key = lowered.translate(str.maketrans('', '', string.punctuation)).strip()

        if key:
            value = recall(key)
            reply = f"You told me your {key} is {value}."
        else:
            reply = "Please ask me something specific you told me earlier."
        
        '''
        
    elif any(x in command.lower() for x in ["what is my", "do you remember", "what do you remember", "what did i tell you"]):
        command_lower = command.lower()
        key = command_lower.replace("what is my", "")\
                       .replace("do you remember", "")\
                       .replace("what do you remember", "")\
                       .replace("what did i tell you", "")\
                       .replace("about", "")\
                       .strip()
        key = key.replace("my", "").strip()  # extra cleanup
        value = recall(key)
        reply = f"You told me your {key} is {value}."
            '''
    
    
    
    
    elif "when i say" in command and "do this" in command:
        try:
            parts = command.split("when i say")[1].strip()
            phrase, action = parts.split("do this")
            phrase = phrase.strip()
            action = action.strip()

            # Load or create
            if not os.path.exists(CUSTOM_FILE):
                custom_map = {}
            else:
                with open(CUSTOM_FILE, "r") as f:
                    custom_map = json.load(f)

            # Save mapping
            custom_map[phrase] = action
            with open(CUSTOM_FILE, "w") as f:
                json.dump(custom_map, f, indent=2)

            reply = f"✅ Got it! When you say '{phrase}', I’ll now: {action}"
        except Exception as e:
            reply = "Couldn't save that command. Please say: 'When i say launch mode, do this open Spotify and VS Code'"

    
    
    elif "what can you do" in command or "list your commands" in command or "what are your features" in command:
        reply = "Here are some things I can do:\n" \
                "- Open websites like YouTube or Google\n" \
                "- Play, pause, and control music\n" \
                "- Set reminders and notes\n" \
                "- Answer questions and chat with you\n" \
                "- Remember facts about you\n" \
                "- Save unknown commands when offline\n" \
                #"- Execute custom commands you set up"
    
    
    # 🎙️ Voice Toggle by Command
    elif any(phrase in command for phrase in ["disable tts", "turn off tts", "disable voice"]):
        from core.config import toggle_tts, is_tts_enabled
        if is_tts_enabled():
            toggle_tts()
            reply = "✅ Voice disabled. I won’t speak until you tell me to enable it again."
        else:
            reply = "Voice is already off."
            
        from GUI.gui_main import sync_tts_switch 
        output_text.after(0, sync_tts_switch)

    elif any(phrase in command for phrase in ["enable tts", "turn on tts", "enable voice"]):
        from core.config import toggle_tts, is_tts_enabled
        if not is_tts_enabled():
            toggle_tts()
            reply = "✅ Voice enabled. I will speak again."
        else:
            reply = "Voice is already on."
            
        from GUI.gui_main import sync_tts_switch
        output_text.after(0, sync_tts_switch)

        
    elif "show loading spinner" in command.lower():
        output_text.insert("end", "🤖 Jarvis: Showing loading spinner for 10 sec...\n")
        output_text.see("end")
        output_text.update()  # Ensure GUI updates immediately
        output_text.after(0, lambda: start_spinner(output_text))
        
        
        def finish_spinner():
            # Stop the spinner after 10 seconds
            output_text.after(0, lambda: stop_spinner(output_text, "Spinner finished!"))
            reply = "How's the loading spinner for you!?"
            type_and_speak_text(output_text, reply)
        output_text.after(10000, finish_spinner)  # Show spinner for 10 seconds
        
        
    elif "shutdown my pc" in command.lower() or "shutdown system" in command.lower():
        reply = "Shutting down your system now."
        speak("Shutting down your system now.")
        threading.Thread(target=lambda: os.system("shutdown /s /t 10"), daemon=True).start()
    
    elif "restart my pc" in command:
        reply ="Restarting your system now."
        speak("Restarting your system now.")
        threading.Thread(target=lambda: os.system("shutdown /r /t 1"), daemon=True).start()  # Run restart in a separate thread to avoid blocking GUI
    
    elif "sleep my pc" in command:
        reply= "Putting your system to sleep."
        speak("Putting your system to sleep.")
        threading.Thread(target=lambda: os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0"), daemon=True).start()  
        
    
    elif "hibernate my pc" in command:
        reply= "Hibernating your system now."
        speak("Hibernating your system now.")
        threading.Thread(target=lambda: os.system("shutdown /h"), daemon=True).start()  # Run hibernate in a separate thread to avoid blocking GUI
  
    
    elif "lock my pc" in command:
        reply = "Locking your system now."
        speak("Locking your system now.")
        
        threading.Thread (target=lambda: os.system("rundll32.exe user32.dll,LockWorkStation"),daemon=True).start()
    
    elif "open folder" in command:
        folder_name = command.replace("open folder", "").strip()
        '''folder_path = os.path.join("C:\\Users\\akhil", folder_name)'''
        folder_path = os.path.join(os.path.expanduser("~"), folder_name) # Use user's home directory to find the folder
        #e.g. #folder_path = os.path.join(os.path.expanduser("~"), "Documents", folder_name) # Example for Documents folder
        if os.path.exists(folder_path):
            speak(f"Opening folder {folder_name}")
            os.startfile(folder_path)
        else:
            speak("Sorry, I couldn't find that folder.")
        
    elif "open my github" in command:
        reply = "Opening Github..."
        
        threading.Thread (target=lambda: webbrowser.open("https://www.github.com"),daemon=True).start()
    
    elif "open my linkedin" in command:
        reply = "Opening LinkedIn..."
        
        threading.Thread (target=lambda: webbrowser.open("https://www.linkedin.com"),daemon=True).start()

    elif "battery status" in command or "battery level" in command:
        battery = psutil.sensors_battery()

        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "on battery power"
            reply = f"System battery is at {percent}%, currently {plugged}."

        else:
            reply = "No battery detected on this system."

    elif "system status" in command or "cpu usage" in command:
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        reply = f"CPU usage is at {cpu}%, and RAM usage is at {ram}%."

    elif "unmute" in command:
        vol = AudioUtilities.GetSpeakers().EndpointVolume
        vol.SetMute(False, None)
        reply = "Audio unmuted."

    elif "mute" in command:
        vol = AudioUtilities.GetSpeakers().EndpointVolume
        vol.SetMute(True, None)
        reply = "Audio muted."

    elif "volume to" in command or "set volume" in command:
        numbers = re.findall(r"\d+", command)
        if numbers:
            level = int(numbers[0])
            level = max(0, min(100, level))

            vol = AudioUtilities.GetSpeakers().EndpointVolume
            vol.SetMasterVolumeLevelScalar(level / 100, None)
            reply = f"Volume set to {level}%."
        else:
            reply = "Please specify a percentage like volume to 50."

    
       
    else:
        def handle_gemini_command(prompt):
            #start_spinner(output_text)  
            output_text.after(0, lambda: start_spinner(output_text))
            # Start spinner safely in GUI
            
            def task(prompt):
                try:
                    nonlocal reply
                    # Modify Gemini prompt if Hindi
                    if language == "hi":
                        prompt = "उत्तर हिंदी में दो:\n" + prompt    
                    response = model.generate_content(prompt)
                    print("Debug: Gemini response:", response.text.strip())  # Debug print
                    reply = response.text.strip()
                    
                except Exception as e:
                    print("Gemini Error:", e)
                    reply = "Sorry, I couldn't think of a response."
                
                    # Log unknown command
                    def log_unknown_command(cmd):
                        with open(UNKNOWN_FILE, "a") as f:
                            f.write(cmd.strip() + "\n")
                    log_unknown_command(command)
                
                
                #stop_spinner(output_text, reply) # Spinner ends
                #lasttasks(command,reply,output_text)  # Call lasttasks to handle reply and logging
                output_text.after(0, lambda: stop_spinner(output_text, reply))
                output_text.after(0, lambda: lasttasks(command, reply, output_text,language))
                

            threading.Thread(target=task(prompt), daemon=True).start()
            # stop the function here, as the reply will be handled in the thread
             
        # If we reach here, it means no known command matched, so we use Gemini to generate a response
        handled_by_gemini= True
        handle_gemini_command(full_prompt)
        return# function to handle gemini call.
        
        
        
        
        
    
    '''def handle_gemini_command(prompt):
        def task():
            try:
                response = model.generate_content(prompt)
                reply = response.text.strip()
            except Exception as e:
                print("Gemini Error:", e)
                reply = "Sorry, I couldn't think of a response."
                # Log unknown command
                log_unknown_command(command)

        threading.Thread(target=task, daemon=True).start()
        return reply'''

    
    
   
    


    



    if not handled_by_gemini:# If Gemini didn't handle it, we can safely call lasttasks
        lasttasks(command, reply, output_text, language) # Calling the function at last to execute that tasks.





