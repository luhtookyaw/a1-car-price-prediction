import os
import pickle
import numpy as np

# Load the model once at the start of the application
model_path = os.path.join(os.path.dirname(__file__), 'model', 'car_price_prediction.model')
with open(model_path, 'rb') as file:
  car_price_model = pickle.load(file)

scaler_path = os.path.join(os.path.dirname(__file__), 'model', 'scaler.pkl')
with open(scaler_path, 'rb') as file:
    scaler = pickle.load(file)

def predict_car_price(input_data):
  """Predict car price based on input data."""
  prediction = car_price_model.predict(input_data)
  return np.exp(prediction[0])

def transform(input_data):
  """Transform input data"""
  tranformed_data = scaler.transform([input_data])
  return tranformed_data