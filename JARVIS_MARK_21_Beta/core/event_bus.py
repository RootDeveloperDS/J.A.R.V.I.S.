"""
event_bus.py - Publish-Subscribe Event Bus for JARVIS System Events & Plugins
"""

import threading

# System Event Constants
EVENT_USER_COMMAND = "user_command"
EVENT_JARVIS_RESPONSE = "jarvis_response"
EVENT_PLUGIN_LOADED = "plugin_loaded"
EVENT_PLUGIN_UNLOADED = "plugin_unloaded"
EVENT_PLUGIN_ERROR = "plugin_error"


class EventBus:
    """Thread-safe Publish-Subscribe Event Bus."""

    def __init__(self):
        self._listeners = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, listener: callable):
        """Subscribe a listener callback to an event type."""
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            if listener not in self._listeners[event_type]:
                self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: str, listener: callable):
        """Unsubscribe a listener callback from an event type."""
        with self._lock:
            if event_type in self._listeners and listener in self._listeners[event_type]:
                self._listeners[event_type].remove(listener)

    def publish(self, event_type: str, payload: dict = None):
        """Publish an event to all subscribed listeners asynchronously/safely."""
        payload = payload or {}
        with self._lock:
            listeners = list(self._listeners.get(event_type, []))

        for listener in listeners:
            try:
                listener(event_type, payload)
            except Exception as e:
                print(f"⚠️ EventBus Error dispatching '{event_type}' to {listener}: {e}")


# Global singleton EventBus instance
event_bus = EventBus()
