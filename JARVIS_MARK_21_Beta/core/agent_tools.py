"""
agent_tools.py - Centralized Agentic Tool Definitions & Dispatcher for Gemini Function Calling
"""

import os
import requests
import json
from features.notes import add_note, load_notes
from features.reminders import add_reminder, add_natural_reminder
from features.music import play_music, pause_music, resume_music, stop_music, next_song, shuffle_music
from api.location import get_city_by_ip

# Tool 1: Weather Tool
def get_weather_data(city: str = "") -> str:
    """Fetch current weather information for a specified city or current location.
    
    Args:
        city: Optional city name. If omitted, detects location by IP.
    """
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return "Weather API key is not configured in .env file."
        
        target_city = city.strip() if city else get_city_by_ip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={target_city}&appid={api_key}&units=metric"
        res = requests.get(url, timeout=5).json()
        
        if res.get("cod") != 200:
            return f"Weather unavailable for '{target_city}'."
        
        temp = res["main"]["temp"]
        feels = res["main"]["feels_like"]
        hum = res["main"]["humidity"]
        desc = res["weather"][0]["description"].title()
        return f"Weather in {target_city}: {temp}°C (Feels like {feels}°C), Humidity: {hum}%, Condition: {desc}."
    except Exception as e:
        return f"Failed to fetch weather: {e}"

# Tool 2: Notes Tool
def save_user_note(note_text: str) -> str:
    """Save a text note to user memory.
    
    Args:
        note_text: The note content to save.
    """
    try:
        add_note(note_text)
        return f"Successfully saved note: '{note_text}'."
    except Exception as e:
        return f"Failed to save note: {e}"

# Tool 3: Reminders Tool
def set_reminder_task(task: str, delay_minutes: int = 15) -> str:
    """Set a time-based reminder for a specific task.
    
    Args:
        task: The task description to be reminded about.
        delay_minutes: Time delay in minutes from now.
    """
    try:
        add_reminder(task, int(delay_minutes))
        return f"Reminder set for '{task}' in {delay_minutes} minutes."
    except Exception as e:
        return f"Failed to set reminder: {e}"

# Tool 4: Music Player Tool
def control_music_player(action: str) -> str:
    """Control the built-in music player.
    
    Args:
        action: The playback command (play, pause, resume, stop, next, shuffle).
    """
    act = action.lower().strip()
    try:
        if act == "play":
            play_music()
            return "Music playback started."
        elif act == "pause":
            pause_music()
            return "Music paused."
        elif act == "resume":
            resume_music()
            return "Music resumed."
        elif act == "stop":
            stop_music()
            return "Music stopped."
        elif act == "next":
            next_song()
            return "Skipped to next song."
        elif act == "shuffle":
            shuffle_music()
            return "Music playlist shuffled and started."
        else:
            return f"Unknown music action '{action}'. Valid actions: play, pause, resume, stop, next, shuffle."
    except Exception as e:
        return f"Failed to perform music action '{action}': {e}"

# Tool 5: Calculator Tool
def calculate_expression(expression: str) -> str:
    """Evaluate a mathematical expression.
    
    Args:
        expression: Math expression to solve, e.g., '25 * 4' or '100 / 5'.
    """
    try:
        allowed_chars = "0123456789+-*/(). "
        clean_expr = "".join([c for c in expression if c in allowed_chars])
        if not clean_expr.strip():
            return "Invalid math expression."
        result = eval(clean_expr, {"__builtins__": None}, {})
        return f"The result of '{clean_expr.strip()}' is {result}."
    except Exception as e:
        return f"Calculation error: {e}"

# Tool 6: System Control Tool
def system_power_control(action: str) -> str:
    """Control host system power states.
    
    Args:
        action: System command (lock, sleep, hibernate, restart, shutdown).
    """
    act = action.lower().strip()
    try:
        if act == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "System locked."
        elif act == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "System entering sleep mode."
        elif act == "hibernate":
            os.system("shutdown /h")
            return "System hibernating."
        elif act == "restart":
            os.system("shutdown /r /t 5")
            return "System restarting in 5 seconds."
        elif act == "shutdown":
            os.system("shutdown /s /t 10")
            return "System shutting down in 10 seconds."
        else:
            return f"Unknown system power command '{action}'."
    except Exception as e:
        return f"Failed system power command '{action}': {e}"


# Tool 7: Vision Screen Tool
def inspect_desktop_screen(prompt: str = "Analyze the current screen") -> str:
    """Capture and analyze the active desktop screen image.
    
    Args:
        prompt: Question or instruction for analyzing the screen.
    """
    from core.vision import get_screen_image
    img = get_screen_image()
    if not img:
        return "Failed to capture desktop screenshot."
    return "Captured screen screenshot for multimodal vision analysis."


# Tool 8: Vision Webcam Tool
def inspect_webcam_snapshot(prompt: str = "Describe what you see in the camera") -> str:
    """Capture and analyze a snapshot frame from the webcam.
    
    Args:
        prompt: Instruction for analyzing the camera frame.
    """
    from core.vision import get_webcam_image
    img = get_webcam_image()
    if not img:
        return "Webcam frame unavailable."
    return "Captured camera snapshot for multimodal vision analysis."


# List of tool functions for Gemini Model registration
AGENT_TOOLS = [
    get_weather_data,
    save_user_note,
    set_reminder_task,
    control_music_player,
    calculate_expression,
    system_power_control,
    inspect_desktop_screen,
    inspect_webcam_snapshot
]

# Tool dispatcher mapping for execution
TOOL_MAP = {
    "get_weather_data": get_weather_data,
    "save_user_note": save_user_note,
    "set_reminder_task": set_reminder_task,
    "control_music_player": control_music_player,
    "calculate_expression": calculate_expression,
    "system_power_control": system_power_control,
    "inspect_desktop_screen": inspect_desktop_screen,
    "inspect_webcam_snapshot": inspect_webcam_snapshot
}

def execute_tool_call(func_name: str, func_args: dict) -> str:
    """Execute a function call returned by Gemini and return string result."""
    if func_name not in TOOL_MAP:
        return f"Error: Tool '{func_name}' is not registered."
    
    try:
        tool_fn = TOOL_MAP[func_name]
        return str(tool_fn(**func_args))
    except Exception as e:
        return f"Error executing tool '{func_name}': {e}"
