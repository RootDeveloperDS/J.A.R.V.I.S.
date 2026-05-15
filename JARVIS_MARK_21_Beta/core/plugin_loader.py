import os
import importlib.util

# Base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute plugins path
PLUGIN_FOLDER = os.path.join(BASE_DIR, "..", "plugins")
PLUGIN_FOLDER = os.path.abspath(PLUGIN_FOLDER)


def load_plugins():
    plugin_registry = {}

    # Safety check
    if not os.path.exists(PLUGIN_FOLDER):
        print(f"[PLUGIN ERROR] Plugin folder not found: {PLUGIN_FOLDER}")
        return plugin_registry

    for filename in os.listdir(PLUGIN_FOLDER):

        if filename.endswith(".py") and filename != "__init__.py":

            plugin_name = filename[:-3]

            filepath = os.path.join(PLUGIN_FOLDER, filename)

            try:
                spec = importlib.util.spec_from_file_location(
                    plugin_name,
                    filepath
                )

                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                if hasattr(module, "register"):

                    plugin = module.register()

                    trigger = plugin["trigger"]

                    plugin_registry[trigger] = plugin

                    print(f"[PLUGIN LOADED] {plugin_name}")

            except Exception as e:
                print(f"[PLUGIN FAILED] {plugin_name}: {e}")

    return plugin_registry