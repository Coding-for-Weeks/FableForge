import importlib
import pkgutil

scene_encounters = {}

for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name.startswith("scene_encounter"):
        module = importlib.import_module(f"{__name__}.{module_name}")
        key = module_name.replace("scene_", "")  # e.g., "scene_encounter1" -> "encounter1"
        scene_encounters[key] = module
