import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .utils import predict_car_price, transform

# Median values for default fields
MEDIAN_VALUES = {
    "year": 2015,
    "engine": 1248,
    "max_power": 82.4
}

@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            body = json.loads(request.body)
            features = body.get('features', [])
            
            year = features[0] if features[0] else MEDIAN_VALUES["year"]
            transmission = features[1]  # Transmission is always required
            engine = features[2] if features[2] else MEDIAN_VALUES["engine"]
            max_power = features[3] if features[3] else MEDIAN_VALUES["max_power"]

            # Validate the inputs
            if not (1994 <= int(year) <= 2020):
                return JsonResponse({"error": "Year must be between 1994 and 2020."}, status=400)
            if not (600 <= int(engine) <= 3700):
                return JsonResponse({"error": "Engine size must be between 600 and 3700 CC."}, status=400)
            if not (30 <= float(max_power) <= 400):
                return JsonResponse({"error": "Max power must be between 30 and 400 HP."}, status=400)

            # Make prediction
            filled_features = [year, transmission, engine, max_power]
            
            # Make prediction
            transformed_features = transform(filled_features)
            predicted_price = predict_car_price(transformed_features)
            return JsonResponse({'predicted_price': predicted_price}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'message': 'Send POST request with features[] data.'}, status=405)

def home_view(request):
    return render(request, 'prediction.html')