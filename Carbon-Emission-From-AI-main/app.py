from flask import Flask, render_template, request, jsonify
from logic import get_token_count, calculate_interaction_pollution, format_car_time
from constant import MODELS, REGIONS

app = Flask(__name__)

@app.route('/')
def index():
    # Providing a default string for the textarea
    default_text = "explain to me these calculus 3 concepts: 1. Vector-valued functions..."
    return render_template('index.html', default_text=default_text)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        # Use force=True to handle cases where Content-Type header might be missing
        data = request.get_json(force=True) 
        
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
            
        # Extract values
        text = data.get('prompt_text', '')
        model = data.get('model', 'GPT-4o (Medium)')
        region = data.get('region', 'Germany')

        # Calculate tokens and pollution
        x = get_token_count(text, model)
        co2_low, co2_high = calculate_interaction_pollution(x, model, region)
        
        # Calculate slopes for the graph
        def get_slope(m_name, r_name):
            tokens_test = 1000
            low, high = calculate_interaction_pollution(tokens_test, m_name, r_name)
            return ((low + high) / 2) / tokens_test

        slopes = {m: get_slope(m, region) for m in MODELS}

        # Projection Helper
        def get_p(days):
            l, h = co2_low * days, co2_high * days
            return {
                "co2": f"{l:.2f} - {h:.2f}",
                "car": f"{format_car_time(l)} - {format_car_time(h)}"
            }

        return jsonify({
            "status": "success",
            "tokens": x,
            "co2_range": f"{co2_low:.4f} - {co2_high:.4f} kg",
            "car_range": f"{format_car_time(co2_low)} - {format_car_time(co2_high)}",
            "slopes": slopes,
            "projections": {
                "mo1": get_p(30),
                "mo6": get_p(180),
                "yr1": get_p(365),
                "yr5": get_p(1825)
            }
        })
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)