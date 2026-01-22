# logic.py
import tiktoken
from constant import MODELS, REGIONS, PUE_SWEDEN, PUE_GERMANY, PUE_USA, K

def get_token_count(text, model_name):
    if not text:
        return 0
    try:
        # Standard encoding for GPT-4 family models
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except:
        # Fallback for simple estimation
        return int(len(text.split()) * 1.3)

def calculate_interaction_pollution(tokens, model_name, region_name):
    # 1. Base energy (y) based on model size
    if "Small" in model_name:
        y = 0.20
    elif "Medium" in model_name:
        y = 0.45
    else:
        y = 0.80

    # 2. Regional Intensity (z) and PUE
    if region_name == "Sweden":
        z, pue = 0.03, PUE_SWEDEN
    elif region_name == "Germany":
        z, pue = 0.35, PUE_GERMANY
    else:
        z, pue = 0.85, PUE_USA

    # 3. Input energy (Initial processing)
    input_co2 = tokens * y * pue * z * K

    # 4. Output energy (3x to 9x range for sequential decoding)
    output_low = input_co2 * 3.0
    output_high = input_co2 * 9.0

    # 5. Total combined interaction
    return (input_co2 + output_low), (input_co2 + output_high)

def format_car_time(co2_kg):
    # Standard car: 0.197kg/km. At 100km/h, 1km = 0.6 mins
    total_minutes = (co2_kg / 0.197) * 0.6
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"