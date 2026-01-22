# Base Energy Factor (y) - Wh/token
MODELS = {
    "GPT-4o mini (Small)": 0.20,
    "GPT-4o (Medium)": 0.45,
    "GPT-4 (Large)": 0.80
}

# Regional Carbon Intensity (z) - kg CO₂/kWh and PUE
REGIONS = {
    "Sweden": 0.03,
    "Germany": 0.35,
    "West Virginia, USA": 0.85
}

PUE_SWEDEN = 1.15
PUE_GERMANY = 1.46 
PUE_USA = 1.58    

# Conversion factor: Wh to kWh
K = 1/1000