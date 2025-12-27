import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)

# Enable CORS so your Vercel frontend can talk to this Render backend
CORS(app, resources={r"/*": {"origins": "*"}})

# --- LOAD YOUR ML MODEL ---
# Update 'food_waste_model.pkl' to match your actual model filename!
MODEL_PATH = 'food_waste_model.pkl'

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    else:
        print(f"WARNING: Model file '{MODEL_PATH}' not found. Predictions will fail.")
        model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "ML API is running", "model_loaded": model is not None}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()
        
        # Extract features (Ensure these match what your model expects!)
        # Example: quantity, days_until_expiry, etc.
        # You might need to adjust this part to match your specific model inputs
        features = [
            data.get('quantity', 0),
            data.get('days_until_expiry', 0),
            # Add other features your model needs here
        ]
        
        # Convert to numpy array for prediction
        prediction_input = np.array([features])
        
        # Make prediction
        prediction = model.predict(prediction_input)
        
        # Return result
        return jsonify({
            "prediction": prediction[0],
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Render requires the app to listen on port 10000 or the $PORT env var
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
