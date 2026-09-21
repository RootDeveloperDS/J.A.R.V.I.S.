"""
plugin_loader.py - Sandboxed Plugin Loader & Dynamic Hot-Reload Engine
"""

import os
import importlib.util
from core.event_bus import event_bus, EVENT_PLUGIN_LOADED, EVENT_PLUGIN_ERROR
from core.base_plugin import BasePlugin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "plugins"))

# Global registry tracking loaded plugin instances & file timestamps
plugin_registry = {}
_file_timestamps = {}


def safe_run_plugin(plugin_entry: dict, command: str, output_widget):
    """Execute a plugin within an exception-isolated sandbox."""
    try:
        run_fn = plugin_entry.get("run")
        if run_fn:
            run_fn(command, output_widget)
    except Exception as e:
        err_msg = f"[PLUGIN ERROR] {plugin_entry.get('name', 'Unknown')}: {e}"
        print(err_msg)
        if output_widget:
            try:
                output_widget.insert("end", f"{err_msg}\n")
                output_widget.see("end")
            except Exception:
                pass
        event_bus.publish(EVENT_PLUGIN_ERROR, {"plugin": plugin_entry.get("name"), "error": str(e)})


def load_plugins():
    """Load all plugin modules from the plugins folder."""
    global plugin_registry, _file_timestamps
    plugin_registry.clear()

    if not os.path.exists(PLUGIN_FOLDER):
        print(f"[PLUGIN ERROR] Plugin folder not found: {PLUGIN_FOLDER}")
        return plugin_registry

    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py") and filename != "__init__.py":
            filepath = os.path.join(PLUGIN_FOLDER, filename)
            _load_single_plugin(filename, filepath)

    return plugin_registry


def _load_single_plugin(filename: str, filepath: str):
    """Load or reload an individual plugin file."""
    plugin_name = filename[:-3]
    try:
        mtime = os.path.getmtime(filepath)
        _file_timestamps[filepath] = mtime

        spec = importlib.util.spec_from_file_location(plugin_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 1. Check for BasePlugin subclass
        plugin_instance = None
        for attr in dir(module):
            val = getattr(module, attr)
            if isinstance(val, type) and issubclass(val, BasePlugin) and val is not BasePlugin:
                plugin_instance = val()
                plugin_instance.on_load()
                event_bus.subscribe("all", plugin_instance.on_event)
                
                plugin_entry = {
                    "trigger": plugin_instance.trigger,
                    "name": plugin_instance.name,
                    "description": plugin_instance.description,
                    "instance": plugin_instance,
                    "run": lambda cmd, widget, inst=plugin_instance: inst.run(cmd, widget)
                }
                plugin_registry[plugin_instance.trigger] = plugin_entry
                print(f"[SDK PLUGIN LOADED] {plugin_instance.name} (trigger: '{plugin_instance.trigger}')")
                event_bus.publish(EVENT_PLUGIN_LOADED, {"name": plugin_instance.name, "trigger": plugin_instance.trigger})
                return

        # 2. Check for legacy register() dict format
        if hasattr(module, "register"):
            plugin_dict = module.register()
            trigger = plugin_dict["trigger"]
            plugin_entry = {
                "trigger": trigger,
                "name": plugin_name,
                "description": plugin_dict.get("description", ""),
                "run": plugin_dict["run"]
            }
            plugin_registry[trigger] = plugin_entry
            print(f"[LEGACY PLUGIN LOADED] {plugin_name} (trigger: '{trigger}')")
            event_bus.publish(EVENT_PLUGIN_LOADED, {"name": plugin_name, "trigger": trigger})

    except Exception as e:
        print(f"[PLUGIN LOAD FAILED] {plugin_name}: {e}")
        event_bus.publish(EVENT_PLUGIN_ERROR, {"plugin": plugin_name, "error": str(e)})


def reload_modified_plugins():
    """Hot-reload any modified plugin files dynamically without restarting app."""
    if not os.path.exists(PLUGIN_FOLDER):
        return

    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py") and filename != "__init__.py":
            filepath = os.path.join(PLUGIN_FOLDER, filename)
            mtime = os.path.getmtime(filepath)
            if filepath not in _file_timestamps or _file_timestamps[filepath] < mtime:
                print(f"[HOT-RELOAD] Detected change in {filename}, reloading...")
                _load_single_plugin(filename, filepath)