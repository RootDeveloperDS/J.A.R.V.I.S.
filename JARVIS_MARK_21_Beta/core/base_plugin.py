"""
base_plugin.py - Standard Plugin Base Class & Lifecycle SDK for JARVIS Plugins
"""

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """Abstract Base Class for JARVIS Plugins."""

    name: str = "Base Plugin"
    trigger: str = "base"
    description: str = "JARVIS Plugin Base"
    version: str = "1.0.0"

    def on_load(self):
        """Called when plugin is loaded into memory."""
        pass

    def on_unload(self):
        """Called when plugin is unloaded or reloaded."""
        pass

    @abstractmethod
    def run(self, command: str, output_widget):
        """Main execution method invoked when trigger keyword is matched."""
        pass

    def on_event(self, event_type: str, payload: dict):
        """Event listener callback invoked by EventBus."""
        pass
