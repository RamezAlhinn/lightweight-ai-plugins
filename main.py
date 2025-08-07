from plugins.light_model import LightModelPlugin
from core.orchestrator import run_pipeline

if __name__ == "__main__":
    input_data = "Hello from main"
    result = run_pipeline(input_data)
    print("Result:", result)