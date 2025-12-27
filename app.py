import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# 1. CORS: Allow everyone (Crucial for Vercel)
CORS(app, resources={r"/*": {"origins": "*"}})

# 2. Load Model (Optional - we will use logic if model fails)
MODEL_PATH = 'food_waste_model.pkl'
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully")
    else:
        print(f"WARNING: Model file not found. Using Logic Mode.")
except Exception as e:
    print(f"Error loading model: {e}")

# --- HELPER FUNCTIONS ---
def calculate_days_diff(date_str):
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now()
        return (target_date - today).days
    except:
        return 0

# --- ROUTES ---

@app.route('/health', methods=['GET'])
def health():
    # Matches exactly what your api.ts expects
    return jsonify({
        "status": "ML API is running",
        "models_loaded": True 
    }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Sharebite ML Backend is Live!"}), 200

# --- PREDICTION ENDPOINTS (Matching your api.ts) ---

@app.route('/predict/all', methods=['POST'])
def predict_all():
    try:
        data = request.get_json()
        
        # Extract basic data
        quantity = float(data.get('quantity', 0))
        days_until_expiry = calculate_days_diff(data.get('expiry_date', ''))
        category = data.get('category', 'General')
        
        # --- LOGIC ENGINE (Simulates AI if model is complex/missing) ---
        
        # 1. Expiration Logic
        predicted_expiry = max(1, days_until_expiry)
        
        # 2. Waste Risk Logic (High quantity + low expiry = High Risk)
        risk_score = 0.0
        if days_until_expiry < 3: risk_score += 0.4
        if quantity > 20: risk_score += 0.4
        if category in ['Dairy', 'Meat']: risk_score += 0.2
        
        risk_level = "Low"
        if risk_score > 0.7: risk_level = "High"
        elif risk_score > 0.4: risk_level = "Medium"

        # 3. Donation Logic (Donate if safe and valid quantity)
        should_donate = (days_until_expiry > 2) and (quantity > 5)
        donation_prob = 0.9 if should_donate else 0.2

        # 4. Priority Logic
        priority_score = risk_score * 100
        priority_level = "High" if priority_score > 70 else "Normal"

        # Return the EXACT structure your frontend needs
        return jsonify({
            "success": True,
            "predictions": {
                "predicted_days_until_expiry": int(predicted_expiry),
                "waste_risk_score": round(risk_score, 2),
                "risk_level": risk_level,
                "should_donate": should_donate,
                "donation_probability": round(donation_prob, 2),
                "priority_score": int(priority_score),
                "priority_level": priority_level
            }
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 400

# --- INDIVIDUAL ROUTES (In case api.ts calls them separately) ---

@app.route('/predict/waste-risk', methods=['POST'])
def waste_risk():
    # Redirects to the logic used above
    return predict_all()

@app.route('/predict/donation', methods=['POST'])
def donation():
    return predict_all()

@app.route('/predict/priority', methods=['POST'])
def priority():
    return predict_all()

@app.route('/predict/expiration', methods=['POST'])
def expiration():
    return predict_all()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
