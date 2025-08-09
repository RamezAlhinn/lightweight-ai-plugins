import psutil

def get_resource_profile():
    return {
        "cpu_load": psutil.cpu_percent(interval=1) / 100.0,
        "available_ram_mb": psutil.virtual_memory().available / (1024 * 1024),
    }