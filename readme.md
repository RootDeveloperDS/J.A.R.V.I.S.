# J.A.R.V.I.S. Mark 21 (Latest) – Personal AI Assistant  
**Built with Python | CustomTkinter | Gemini API | Modern GUI**

Welcome to **JARVIS Mark 21**, a voice-enabled, GUI-based personal AI assistant inspired by Iron Man's JARVIS — reimagined and developed by **Devansh**. This assistant is smart, stylish, and customizable — perfect for everyday automation, chatting, and cool AI experiments!

---

## ✨ Features

### 🎨 **User Interface & Experience**
- **Modern GUI (CustomTkinter)** – Beautiful dark-mode interface with customizable themes
- **Animated Avatar** – Live animated assistant face (supports GIF, PNG, JPG formats)
- **Video Intro** – Cinematic startup video with fade-out effects
- **Productivity Dashboard** – Left sidebar with calendar, clock, and uptime timer
- **RGB Sidebar Border** – Dynamic color-cycling border for a techy look
- **Theme System** – Multiple pre-built themes to customize your experience
- **Custom Backgrounds** – Set your own background images
- **Loading Animations** – Smooth spinner animations during AI processing
- **Typing Animation** – Cinematic text typing with random speed variations

### 🎙️ **Voice & Speech**
- **Voice Recognition** – Speech-to-text using SpeechRecognition library
- **Wake Word Detection** – "Hey Jarvis" trigger (toggleable via GUI switch)
- **Text-to-Speech (TTS)** – Voice responses using pyttsx3 (toggleable on/off)
- **Multi-language Support** – Supports English and Hindi language responses
- **Speech Interrupt** – Stop Jarvis mid-speech with interrupt button
- **Voice Toggle** – Enable/disable voice via command or GUI switch

### 🤖 **AI & Intelligence**
- **Gemini API Integration** – Powered by Google's Gemini AI for intelligent conversations
- **Contextual Memory** – Remembers last 20 conversations for context-aware responses
- **Persistent Chat History** – All conversations saved and loaded automatically
- **Smart Memory System** – Remembers personal facts about you (name, preferences, etc.)
- **Natural Language Processing** – Understands commands in natural language

### 📝 **Productivity Features**
- **Notes System** – Add, view, and delete notes
- **Reminders** – Set time-based reminders with natural language support
  - Time delay: "remind me to take medicine in 15 minutes"
  - Natural language: "remind me to call mom tomorrow at 5PM"
- **Custom Commands** – Teach Jarvis new commands: "when i say X, do this Y"
- **Chat History** – View and save conversation history
- **Memory Recall** – Ask "what is my name?" or "do you remember my birthday?"

### 🎵 **Media & Entertainment**
- **Music Player** – Play, pause, resume, stop, skip, and shuffle music
- **Auto Music Detection** – Automatically loads music from your Music folder
- **Background Music** – Play music while using other features

### 🌐 **Web & System Integration**
- **Web Browser Control** – Open websites (YouTube, Google, GitHub, LinkedIn)
- **System Commands** – Control your PC with voice/text:
  - Shutdown: "shutdown my pc"
  - Restart: "restart my pc"
  - Sleep: "sleep my pc"
  - Hibernate: "hibernate my pc"
  - Lock: "lock my pc"
- **Folder Navigation** – Open folders by name
- **Application Launcher** – Launch applications via custom commands

### 🌤️ **Real-time Information**
- **Weather Updates** – Live weather information with auto-location detection
  - Current temperature, feels-like, humidity
  - Weather description with emoji indicators
  - Auto-refreshes every minute
- **Tech News** – Latest technology news from NewsAPI and HackerNews
  - Top 5 tech headlines displayed in sidebar
  - Auto-refreshes periodically
- **Market Watch** – Stock market data display (in right sidebar)

### 🧮 **Utilities & Plugins**
- **Calculator Plugin** – Advanced math calculations via voice/text
  - Supports: addition, subtraction, multiplication, division
  - Percentage calculations: "increase 100 by 10%"
  - Natural language: "what is 25 plus 17?"
- **Plugin System** – Modular plugin architecture for easy extensions
  - Create custom plugins with simple registration
  - Auto-loads all plugins from `plugins/` folder

### 🎯 **Advanced Features**
- **Auto-Learning Mode** – Jarvis learns custom commands from you
- **Bold Text Formatting** – Text in asterisks automatically becomes bold
- **Enter Key Support** – Send messages with Enter key
- **Unknown Command Logging** – Saves unrecognized commands for future learning
- **Thread-Safe Operations** – All operations run in background threads (no freezing)
- **Error Handling** – Graceful error handling with user-friendly messages

---

## 🧠 Tech Stack

### Core Technologies
- **Python 3.12+** – Programming language
- **CustomTkinter** – Modern GUI framework
- **Google Gemini API** – AI conversation engine
- **SpeechRecognition** – Voice input processing
- **pyttsx3** – Text-to-speech engine

### Key Libraries
- **Pillow (PIL)** – Image processing for avatars
- **requests** – HTTP requests for APIs
- **python-dotenv** – Environment variable management
- **pygame** – Music playback
- **OpenCV (cv2)** – Video intro playback
- **BeautifulSoup4** – Web scraping (if needed)

---

## 📁 Project Structure

```
JARVIS_MARK_21_Beta/
├── JarvisMain.py              # Main entry point
├── video_intro.py             # Startup video handler
├── floating_button.py         # Optional floating button
├── .env                       # API keys (create this file)
├── requirements.txt           # Python dependencies
│
├── GUI/                       # User Interface
│   ├── __init__.py
│   ├── gui_main.py           # Main GUI window
│   ├── avatar.py             # Avatar display handler
│   ├── helper.py             # GUI helper functions
│   └── themes/
│       └── themes.py         # Theme definitions
│
├── core/                      # Core Logic
│   ├── commands.py           # Command processing
│   ├── utils.py              # Utility functions
│   ├── memory.py             # Memory management
│   ├── config.py             # Configuration settings
│   ├── theme_manager.py      # Theme management
│   └── plugin_loader.py      # Plugin system loader
│
├── features/                  # Feature Modules
│   ├── notes.py              # Notes management
│   ├── reminders.py          # Reminder system
│   └── music.py              # Music player
│
├── voice/                    # Speech & Voice
│   ├── tts.py                # Text-to-speech
│   └── stt.py                # Speech-to-text
│
├── api/                       # External API Integrations
│   ├── gemini.py             # Gemini AI integration
│   ├── weather.py            # Weather API
│   ├── news.py               # News API
│   ├── location.py           # Location detection
│   └── stock_data.py         # Stock market data
│
├── plugins/                   # Plugin System
│   ├── __init__.py
│   └── calculator.py         # Calculator plugin
│
├── DATA/                      # User Data Storage
│   ├── notes.json            # Saved notes
│   ├── reminders.json        # Saved reminders
│   ├── chat_log.txt          # Conversation history
│   ├── memory.json           # Persistent memory
│   ├── custom_commands.json  # Learned commands
│   └── unknown_commands.txt  # Unrecognized commands
│
└── assets/                    # Media Assets
    ├── intro.mp4             # Startup video
    ├── avatar*.gif           # Avatar animations
    └── jarvis_bg.*           # Background images
```

---

## ⚙️ Setup Instructions

### Prerequisites
- **Python 3.12 or higher** installed on your system
- **Microphone** (for voice features)
- **Internet connection** (for AI and API features)

### Step-by-Step Installation

#### 1. **Clone the Repository**
```bash
git clone https://github.com/RootDeveloperDS/J.A.R.V.I.S..git
cd J.A.R.V.I.S.
```

#### 2. **Install Python Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt
```

**Note for Windows users:** If you encounter issues with `PyAudio`, try:
```bash
pip install pipwin
pipwin install pyaudio
```

#### 3. **Set Up API Keys**

run **JarvisMain.py** and enter your API key when asked:

```env
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Optional API Keys (for additional features)
WEATHER_API_KEY=your_openweathermap_api_key
NEWS_API_KEY=your_newsapi_key
```

**How to get API keys:**
- **Gemini API**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get your free API key
- **Weather API** (optional): Get from [OpenWeatherMap](https://openweathermap.org/api)
- **News API** (optional): Get from [NewsAPI](https://newsapi.org/)

#### 4. **Configure Music Folder (Optional)**

By default, Jarvis looks for music in your system's Music folder. To change this, edit `features/music.py` and update the path.

#### 5. **Run JARVIS**

```bash
python JarvisMain.py
```

**First Run:**
- You'll see a startup video intro (press ESC to skip)
- The GUI will launch with a welcome message
- Jarvis will check for API keys and create necessary data files

---

## 🎮 Usage Guide

### Basic Commands

#### **Voice Commands**
1. **Enable Wake Word**: Toggle the "Wake Word" switch in GUI
2. **Say "Hey Jarvis"** to activate voice mode
3. **Speak your command** after hearing the activation sound
4. **Jarvis will respond** both in text and voice

#### **Text Commands**
1. Type your message in the input box
2. Press **Enter** or click **Send**
3. Jarvis responds in the chat window

### Common Commands

#### **Chat & Questions**
- Ask any question: "What is artificial intelligence?"
- General conversation: "Tell me a joke"
- Language support: Ask in Hindi for Hindi responses

#### **Notes & Reminders**
- `"add note [your note]"` – Save a note
- `"show notes"` – View all notes
- `"delete note [note text]"` – Remove a note
- `"remind me to [task] in [X] minutes"` – Set a reminder
- `"remind me to [task] tomorrow at [time]"` – Natural language reminder
- `"view reminders"` – See all active reminders

#### **Music Control**
- `"play music"` – Start playing music
- `"pause music"` – Pause playback
- `"resume music"` – Continue playback
- `"stop music"` – Stop playback
- `"next song"` – Skip to next track
- `"shuffle music"` – Shuffle playlist

#### **System Control**
- `"shutdown my pc"` – Shutdown computer (10 second delay)
- `"restart my pc"` – Restart computer
- `"sleep my pc"` – Put computer to sleep
- `"hibernate my pc"` – Hibernate computer
- `"lock my pc"` – Lock screen

#### **Web & Apps**
- `"open youtube"` – Open YouTube
- `"open google"` – Open Google
- `"open my github"` – Open GitHub
- `"open my linkedin"` – Open LinkedIn
- `"open folder [folder name]"` – Open folder from home directory

#### **Memory & Learning**
- `"remember that my [key] is [value]"` – Save personal info
  - Example: "remember that my name is John"
- `"what is my [key]"` – Recall saved info
- `"what do you remember"` – See all saved memories
- `"when i say [phrase], do this [action]"` – Teach custom command
  - Example: "when i say launch mode, do this open Spotify and VS Code"

#### **Calculator**
- `"calculator [expression]"` – Perform calculations
  - Examples:
    - "calculator 25 plus 17"
    - "calculator 100 times 5"
    - "calculator increase 100 by 10%"
    - "calculator 50% of 200"

#### **Voice Settings**
- `"enable tts"` or `"turn on tts"` – Enable voice responses
- `"disable tts"` or `"turn off tts"` – Disable voice responses

#### **Utilities**
- `"show chat history"` – Display conversation history
- `"save chat"` – Save current chat to file
- `"what can you do"` – List all available features

---

## 🎨 Customization

### Changing Themes
1. Click **Menu** → **Themes** (or use theme button)
2. Select from available themes
3. Theme is saved and applied on next restart

### Custom Background
1. Place your background image in `assets/` folder
2. Name it `jarvis_bg.png` (or `.jpg`)
3. Restart Jarvis to see the new background

### Avatar Customization
1. Replace avatar files in the main directory:
   - `avatar2.gif`, `avatar4.gif`, `avatar6.gif`, `avatar9.gif`
2. Supported formats: GIF, PNG, JPG
3. Restart Jarvis to load new avatar

### Music Folder
Edit `features/music.py` and change the `MUSIC_FOLDER` path to your preferred music directory.

---

## 🔧 Troubleshooting

### Common Issues

#### **"No module named 'customtkinter'"**
```bash
pip install customtkinter
```

#### **Microphone not working**
- Check microphone permissions in Windows Settings
- Ensure microphone is not being used by another application
- Try running as administrator

#### **API Key Errors**
- Verify `.env` file exists in the correct directory
- Check that API key is correctly formatted (no extra spaces)
- Ensure you have internet connection

#### **Music not playing**
- Verify music files are in supported formats (MP3, WAV)
- Check that music folder path is correct
- Ensure pygame is installed: `pip install pygame`

#### **Avatar not displaying**
- Check that avatar file exists in the directory
- Supported formats: GIF, PNG, JPG
- Try using a different avatar file

#### **Voice recognition not working**
- Check microphone is connected and working
- Install PyAudio: `pip install pyaudio` or `pipwin install pyaudio`
- Try speaking more clearly and louder

---

## 📚 For Developers

### Adding Custom Plugins

1. Create a new file in `plugins/` folder (e.g., `my_plugin.py`)
2. Use this template:

```python
# plugins/my_plugin.py

from voice.tts import speak

def register():
    return {
        "trigger": "mytrigger",  # Word that activates plugin
        "description": "My custom plugin",
        "run": run_my_plugin
    }

def run_my_plugin(command, output_widget):
    # Your plugin logic here
    response = "Plugin executed!"
    output_widget.insert("end", response + "\n")
    output_widget.see("end")
    speak(response)
```

3. Restart Jarvis - plugin will auto-load!

### Extending Commands

Edit `core/commands.py` to add new built-in commands. Follow the existing pattern:

```python
elif "my command" in command:
    reply = "Command response"
    # Your logic here
```

### Modifying GUI

- Main GUI: `GUI/gui_main.py`
- Themes: `GUI/themes/themes.py`
- Avatar: `GUI/avatar.py`

---

## 🔒 API Keys & Security

### Required Keys
- **GEMINI_API_KEY** – Required for AI conversations

### Optional Keys
- **WEATHER_API_KEY** – For weather features
- **NEWS_API_KEY** – For tech news feed

### Security Notes
- Never commit your `.env` file to version control
- Keep API keys private and secure
- Rotate keys if compromised
- The `.env` file is already in `.gitignore`

---

## 🚀 Future Plans (For New Contributors)

- **DevX AI Core Integration** – Custom AI framework
- **Enhanced GUI Animations** – More fluid UI transitions
- **Mobile Port** – Kivy or BeeWare mobile app
- **Web Interface** – Browser-based access
- **Advanced Plugin System** – Plugin marketplace
- **Voice Cloning** – Custom voice profiles
- **Multi-user Support** – Multiple user profiles
- **Cloud Sync** – Sync data across devices
- **More Games & Utilities** – Built-in games and tools

---

## 🔭 Next — VISAR EDGE (coming soon)

**VISAR EDGE V1.0** is on the horizon — the evolution of JARVIS into a more powerful, context-aware, and visually stunning AI environment ecosystem.  
A new chapter of intelligence, design, and autonomy is coming soon...  
**Get ready — the VISAR EDGE Era is about to begin. 🚀**
---

## 📊 Version History

### Mark 21 (Current)
- ✅ Market Watch in sidebar
- ✅ Enhanced plugin system
- ✅ Improved error handling
- ✅ Better UI responsiveness

### Previous Versions
See `All Version Update Details.md` for complete changelog from Mark 6 to Mark 21.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution
- Bug fixes
- New features
- Documentation improvements
- Plugin development
- UI/UX enhancements
- Performance optimizations

---

## 🐛 Reporting Issues

Found a bug? Have a feature request?

1. Check existing [Issues](https://github.com/RootDeveloperDS/JARVIS-AI/issues)
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)

---

## 📖 Documentation

- **Setup Guide**: This README
- **Version History**: `All Version Update Details.md`
- **Code Comments**: Inline documentation in source files

---

## 🙌 Credits

**Developed by:** Devansh Sharma  
**Inspired by:** Iron Man's JARVIS  
**Built with:** Python, CustomTkinter, Gemini API

---

## 📫 Connect With Me

- **GitHub**: [@RootDeveloperDS](https://github.com/RootDeveloperDS)
- **LinkedIn**: [devanshsharma987](https://www.linkedin.com/in/devanshsharma987)
- **Email**: developersofroot@gmail.com

---

## 📜 License

**MIT License** – Feel free to use, modify, and build upon this project. Attribution is appreciated!

```
Copyright (c) 2024 Devansh Sharma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## ⭐ Show Your Support

If you find this project helpful, please consider:
- ⭐ **Starring** the repository
- 🍴 **Forking** for your own use
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 📢 **Sharing** with others

---

**Made with ❤️ by Devansh Sharma**

*"Sometimes you gotta run before you can walk."* – Tony Stark


[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/RootDeveloperDS/J.A.R.V.I.S.)
