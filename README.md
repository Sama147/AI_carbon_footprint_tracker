# AI_carbon_footprint_tracker
A high-fidelity carbon tracking application that models the environmental impact of Large Language Model (LLM) interactions. This tool goes beyond simple estimation by calculating the **Full Interaction Lifecycle**, including sequential decoding multipliers and regional energy grid variables.

 #Key Features

* **Dynamic Token Estimation**: Real-time tokenization using the `cl100k_base` encoding.
* **Multivariable Modeling**: Tracks the complex relationship between prompt length (), model energy demand (), regional grid intensity (), and infrastructure efficiency ().
* **Long-Term Habit Analysis**: Projects carbon accumulation and "Car Time" equivalents over 1 month to 5 years.
* **Interactive Gradient Visualization**: Real-time graphing of carbon emission slopes across different AI model tiers.

## 🧮 Mathematical Framework

The core engine treats carbon emission () as a **Scalar Field** in a 4-dimensional parameter space:
**The Slope as a Partial Derivative**: Each line on the graph represents , measuring the rate of carbon accumulation per token.
**Zero Curvature**: Since , the model demonstrates a constant gradient, resulting in linear growth.
**Sensitivity Analysis**: Switching regions or models effectively evaluates  or , demonstrating how the environmental impact scales with grid intensity and model architecture.

## Project Structure

```text
/Carbon-Emission-From-AI-main
│   app.py          # Flask Server & API Routes
│   logic.py        # Carbon Calculation & Tokenization Logic
│   constant.py     # Regional & Model Intensity Coefficients
├── templates/
│   └── index.html  # Tailwind CSS Dashboard
└── static/
    ├── app.js      # Chart.js Implementation & API Handling
    └── css/
        └── styles.css # Custom UI Styling

```

## ⚙️ Installation & Usage
1. **Install dependencies:**
```bash
pip install flask tiktoken

```
2. **Run the application:**
```bash
python app.py

```
3. **Access the Dashboard:** Navigate to `http://127.0.0.1:5000` in your web browser.

 📊 Data Sources used for the program
* **Energy Intensity**: Based on Wh/token estimates for GPT-4 tier models.
* **Carbon Intensity**: Regional data for Sweden (0.03), Germany (0.35), and USA (0.85) kg /kWh.
* **PUE Factors**: Power Usage Effectiveness coefficients for global data centers.

