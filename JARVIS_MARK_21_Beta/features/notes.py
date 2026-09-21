import os
import json

NOTES_FILE = os.path.join("DATA", "notes.json")

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_notes(notes):
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

def add_note(note):
    notes = load_notes()
    notes.append(note)
    save_notes(notes)

def delete_note(note):
    notes = load_notes()
    if note in notes:
        notes.remove(note)
        save_notes(notes)
        return True
    return False
