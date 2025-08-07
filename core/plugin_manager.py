from plugins.light_model import LightModelPlugin
# Later, import others dynamically

def load_plugin(name: str):
    if name == "light":
        return LightModelPlugin()
    # You can extend for "medium", "heavy"
    raise ValueError(f"No plugin found for {name}")