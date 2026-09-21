import os
import json
from core.vector_memory import add_to_vector_memory, get_rag_context

CHAT_LOG_FILE = os.path.join("DATA", "chat_log.txt")
MEMORY_FILE = os.path.join("DATA", "memory.json")

conversation_history = []  # stores conversation history in memory


def load_conversation_history():
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

            user, jarvis = "", ""
            for line in lines:
                if line.startswith("You:"):
                    user = line.replace("You:", "").strip()
                elif line.startswith("Jarvis:"):
                    jarvis = line.replace("Jarvis:", "").strip()
                    if user and jarvis:
                        conversation_history.append({"user": user, "jarvis": jarvis})
                        user, jarvis = "", ""


def save_conversation_history():
    os.makedirs("DATA", exist_ok=True)
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as file:
        for item in conversation_history:
            file.write(f"You: {item['user']}\nJarvis: {item['jarvis']}\n\n")


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except Exception:
                return {}
    return {}


def save_memory(memory):
    os.makedirs("DATA", exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def remember(key, value):
    memory = load_memory()
    memory[key.lower()] = value
    save_memory(memory)
    # Automatically index fact into vector memory
    add_to_vector_memory(f"Fact about user: {key} = {value}", category="fact")


def recall(key):
    memory = load_memory()
    val = memory.get(key.lower())
    if val:
        return val
    # Fallback to vector search if direct key not found
    rag_ctx = get_rag_context(key)
    if rag_ctx:
        return f"Based on my long-term memory:\n{rag_ctx}"
    return "I don't remember that yet."