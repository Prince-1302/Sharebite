# ML Models for Food Waste Management

This directory contains machine learning models for predicting food expiration, waste risk, donation recommendations, and priority scoring.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Generate Dataset
```bash
python generate_dataset.py
```
This will create `food_waste_dataset.csv` with synthetic food waste data.

### Step 2: Train Models
```bash
python train_models.py
```
This will train 4 models and save them to the `models/` directory:
- `expiration_predictor.joblib` - Predicts days until expiration
- `waste_risk_predictor.joblib` - Predicts waste risk (0-100)
- `donation_recommender.joblib` - Recommends if item should be donated
- `priority_scorer.joblib` - Calculates priority score (0-100)

### Step 3: Start API Server
```bash
python ml_api.py
```
The API will run on `http://localhost:5000`

## API Endpoints

- `GET /health` - Health check
- `POST /predict/expiration` - Predict days until expiration
- `POST /predict/waste-risk` - Predict waste risk score
- `POST /predict/donation` - Recommend donation
- `POST /predict/priority` - Calculate priority score
- `POST /predict/all` - Get all predictions at once

### Example Request:
```json
{
  "category": "Fruits",
  "restaurant_type": "Fast Food",
  "quantity": 50,
  "purchase_date": "2024-01-01",
  "expiry_date": "2024-01-10"
}
```




