def select_model(profile):
    if profile["available_ram_mb"] < 2000 or profile["cpu_load"] > 0.8:
        return "light_model"
    elif profile["available_ram_mb"] >= 8000 and profile["cpu_load"] < 0.5:
        return "heavy_model"
    else:
        return "medium_model"