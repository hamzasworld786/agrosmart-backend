# import joblib
# import os
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .pesticide_knowledge import find_pesticide
# from .weather_service import get_weather, get_farming_advice
# from .blockchain_service import blockchain_service

# api_dir = os.path.dirname(os.path.abspath(__file__))

# # ========== LOAD CROP MODELS ==========
# crop_model = None
# crop_encoder = None
# try:
#     crop_model = joblib.load(os.path.join(api_dir, 'crop_model.pkl'))
#     crop_encoder = joblib.load(os.path.join(api_dir, 'crop_label_encoder.pkl'))
#     print("✅ Crop model loaded")
# except Exception as e:
#     print(f"⚠️ Crop model error: {e}")

# # ========== LOAD FERTILIZER MODELS (FINAL) ==========
# fertilizer_model = None
# fertilizer_target_encoder = None
# fertilizer_features = None
# fertilizer_categorical_cols = None
# fertilizer_encoders = {}

# try:
#     fertilizer_model = joblib.load(os.path.join(api_dir, 'fertilizer_model_final.pkl'))
#     fertilizer_target_encoder = joblib.load(os.path.join(api_dir, 'fertilizer_target_encoder_final.pkl'))
#     fertilizer_features = joblib.load(os.path.join(api_dir, 'fertilizer_features_final.pkl'))
#     fertilizer_categorical_cols = joblib.load(os.path.join(api_dir, 'fertilizer_categorical_cols_final.pkl'))
    
#     # Load encoders for categorical columns
#     for col in fertilizer_categorical_cols:
#         encoder_path = os.path.join(api_dir, f'fertilizer_encoder_{col.replace(" ", "_")}.pkl')
#         if os.path.exists(encoder_path):
#             fertilizer_encoders[col] = joblib.load(encoder_path)
    
#     print(f"✅ Fertilizer model loaded. Expects: {fertilizer_features}")
# except Exception as e:
#     print(f"⚠️ Fertilizer model error: {e}")

# # ========== API ENDPOINTS ==========

# @api_view(['POST'])
# def test_api(request):
#     return Response({'status': 'success', 'message': 'AgroSmart API is working!'})

# @api_view(['POST'])
# def crop_recommendation(request):
#     try:
#         data = request.data
#         features = [float(data[x]) for x in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
#         pred_num = crop_model.predict([features])[0]
#         crop_name = crop_encoder.inverse_transform([pred_num])[0]
#         return Response({'status': 'success', 'recommended_crop': crop_name})
#     except Exception as e:
#         return Response({'status': 'error', 'message': str(e)}, status=400)

# @api_view(['POST'])
# def fertilizer_recommendation(request):
#     try:
#         if fertilizer_model is None:
#             return Response({'status': 'error', 'message': 'Model not loaded'}, status=500)
        
#         data = request.data
        
#         # Build features in the exact order
#         features = []
#         for col in fertilizer_features:
#             # Get value (handle exact column names including spaces)
#             value = data.get(col)
#             if value is None:
#                 return Response({
#                     'status': 'error',
#                     'message': f'Missing field: "{col}"',
#                     'required_fields': fertilizer_features
#                 }, status=400)
            
#             # Encode categorical columns
#             if col in fertilizer_categorical_cols:
#                 encoder = fertilizer_encoders.get(col)
#                 if encoder:
#                     value = encoder.transform([str(value)])[0]
#                 else:
#                     value = str(value)
#             else:
#                 value = float(value)
            
#             features.append(value)
        
#         # Predict
#         pred_num = fertilizer_model.predict([features])[0]
#         fertilizer_name = fertilizer_target_encoder.inverse_transform([pred_num])[0]
        
#         return Response({
#             'status': 'success',
#             'recommended_fertilizer': fertilizer_name,
#             'input_data': data
#         })
        
#     except Exception as e:
#         return Response({'status': 'error', 'message': str(e)}, status=500)

# @api_view(['POST'])
# def pesticide_recommendation(request):
#     """
#     Pesticide Recommendation API
#     Expects JSON: { "crop": "rice", "problem": "leaves have brown spots with gray centers" }
#     """
#     try:
#         data = request.data
        
#         crop = data.get('crop')
#         problem = data.get('problem')
        
#         if not crop:
#             return Response({
#                 'status': 'error',
#                 'message': 'Missing field: crop'
#             }, status=400)
        
#         if not problem:
#             return Response({
#                 'status': 'error',
#                 'message': 'Missing field: problem'
#             }, status=400)
        
#         # Get recommendation from knowledge base
#         recommendation = find_pesticide(crop, problem)
        
#         return Response({
#             'status': 'success',
#             'crop': crop,
#             'problem_description': problem,
#             'recommendation': recommendation
#         })
        
#     except Exception as e:
#         return Response({
#             'status': 'error',
#             'message': str(e)
#         }, status=500)

# @api_view(['POST'])
# def weather_tips(request):
#     """
#     Weather Based Farming Tips API
#     Expects JSON: { "lat": 31.5204, "lon": 74.3587, "crop": "wheat" }
#     """
#     try:
#         data = request.data
        
#         lat = data.get('lat')
#         lon = data.get('lon')
#         crop = data.get('crop', None)
        
#         if not lat or not lon:
#             return Response({
#                 'status': 'error',
#                 'message': 'Missing fields: lat and lon (latitude, longitude)'
#             }, status=400)
        
#         # Get weather data
#         weather = get_weather(lat, lon)
        
#         if not weather:
#             return Response({
#                 'status': 'error',
#                 'message': 'Unable to fetch weather data. Check your OpenWeatherMap API key.'
#             }, status=500)
        
#         # Get AI advice
#         advice = get_farming_advice(weather, crop)
        
#         return Response({
#             'status': 'success',
#             'location': weather['location'],
#             'weather': {
#                 'temperature': weather['temperature'],
#                 'humidity': weather['humidity'],
#                 'conditions': weather['description'],
#                 'wind_speed': weather['wind_speed']
#             },
#             'farming_advice': advice
#         })
        
#     except Exception as e:
#         return Response({
#             'status': 'error',
#             'message': str(e)
#         }, status=500)

#after block chain
import joblib
import os
import json
import socket
import threading
from urllib.parse import urlparse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .pesticide_knowledge import find_pesticide
from .weather_service import get_weather, get_farming_advice
from .blockchain_service import blockchain_service
from .tasks import log_recommendation_task

def is_celery_broker_online():
    """
    Performs a quick TCP socket connection check to see if the Celery broker
    is reachable. This prevents blocking calls to Celery when Redis is offline.
    """
    try:
        broker_url = getattr(settings, 'CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
        parsed = urlparse(broker_url)
        host = parsed.hostname or '127.0.0.1'
        port = parsed.port or 6379
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.02)  # 20ms connection timeout
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def trigger_async_blockchain_log(type_name, recommendation, input_data):
    """
    Triggers the blockchain logging asynchronously.
    First tries to dispatch to the Celery task runner.
    If the broker is offline or Redis is not running, it falls back to
    running in a background daemon thread to maintain sub-50ms response times.
    """
    input_data_json = json.dumps(input_data)
    
    # Perform a quick socket check to bypass Celery if the broker is offline
    if is_celery_broker_online():
        try:
            # Attempt to queue the Celery task asynchronously with retry=False to fail immediately if broker is offline
            log_recommendation_task.apply_async(
                args=(type_name, recommendation, input_data_json),
                retry=False
            )
            print(f"✅ Dispatched {type_name} blockchain log task to Celery queue.")
            return
        except Exception as celery_error:
            print(f"⚠️ Celery dispatch failed: {celery_error}. Falling back to background Python thread.")
    else:
        print("⚠️ Celery broker is offline. Falling back directly to background Python thread.")
        
    # Fallback: run the Web3 logging task in a daemon thread so it runs in the background
    t = threading.Thread(
        target=blockchain_service.log_recommendation,
        args=(type_name, recommendation, input_data_json),
        daemon=True
    )
    t.start()

api_dir = os.path.dirname(os.path.abspath(__file__))

# ========== LOAD CROP MODELS ==========
crop_model = None
crop_encoder = None
try:
    crop_model = joblib.load(os.path.join(api_dir, 'crop_model.pkl'))
    crop_encoder = joblib.load(os.path.join(api_dir, 'crop_label_encoder.pkl'))
    print("✅ Crop model loaded")
except Exception as e:
    print(f"⚠️ Crop model error: {e}")

# ========== LOAD FERTILIZER MODELS (FINAL) ==========
fertilizer_model = None
fertilizer_target_encoder = None
fertilizer_features = None
fertilizer_categorical_cols = None
fertilizer_encoders = {}

try:
    fertilizer_model = joblib.load(os.path.join(api_dir, 'fertilizer_model_final.pkl'))
    fertilizer_target_encoder = joblib.load(os.path.join(api_dir, 'fertilizer_target_encoder_final.pkl'))
    fertilizer_features = joblib.load(os.path.join(api_dir, 'fertilizer_features_final.pkl'))
    fertilizer_categorical_cols = joblib.load(os.path.join(api_dir, 'fertilizer_categorical_cols_final.pkl'))
    
    # Load encoders for categorical columns
    for col in fertilizer_categorical_cols:
        encoder_path = os.path.join(api_dir, f'fertilizer_encoder_{col.replace(" ", "_")}.pkl')
        if os.path.exists(encoder_path):
            fertilizer_encoders[col] = joblib.load(encoder_path)
    
    print(f"✅ Fertilizer model loaded. Expects: {fertilizer_features}")
except Exception as e:
    print(f"⚠️ Fertilizer model error: {e}")

# ========== API ENDPOINTS ==========

@api_view(['POST'])
def test_api(request):
    return Response({'status': 'success', 'message': 'AgroSmart API is working!'})

@api_view(['POST'])
def crop_recommendation(request):
    try:
        data = request.data
        features = [float(data[x]) for x in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        pred_num = crop_model.predict([features])[0]
        crop_name = crop_encoder.inverse_transform([pred_num])[0]
        
        # Log to blockchain asynchronously
        trigger_async_blockchain_log(
            type_name='crop',
            recommendation=crop_name,
            input_data=data
        )
        
        return Response({
            'status': 'success', 
            'recommended_crop': crop_name,
            'input_data': data
        })
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)

@api_view(['POST'])
def fertilizer_recommendation(request):
    try:
        if fertilizer_model is None:
            return Response({'status': 'error', 'message': 'Model not loaded'}, status=500)
        
        data = request.data
        
        # Build features in the exact order
        features = []
        for col in fertilizer_features:
            # Get value (handle exact column names including spaces)
            value = data.get(col)
            if value is None:
                return Response({
                    'status': 'error',
                    'message': f'Missing field: "{col}"',
                    'required_fields': fertilizer_features
                }, status=400)
            
            # Encode categorical columns
            if col in fertilizer_categorical_cols:
                encoder = fertilizer_encoders.get(col)
                if encoder:
                    value = encoder.transform([str(value)])[0]
                else:
                    value = str(value)
            else:
                value = float(value)
            
            features.append(value)
        
        # Predict
        pred_num = fertilizer_model.predict([features])[0]
        fertilizer_name = fertilizer_target_encoder.inverse_transform([pred_num])[0]
        
        # Log to blockchain asynchronously
        trigger_async_blockchain_log(
            type_name='fertilizer',
            recommendation=fertilizer_name,
            input_data=data
        )
        
        return Response({
            'status': 'success',
            'recommended_fertilizer': fertilizer_name,
            'input_data': data
        })
        
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

@api_view(['POST'])
def pesticide_recommendation(request):
    """
    Pesticide Recommendation API
    Expects JSON: { "crop": "rice", "problem": "leaves have brown spots with gray centers" }
    """
    try:
        data = request.data
        
        crop = data.get('crop')
        problem = data.get('problem')
        
        if not crop:
            return Response({
                'status': 'error',
                'message': 'Missing field: crop'
            }, status=400)
        
        if not problem:
            return Response({
                'status': 'error',
                'message': 'Missing field: problem'
            }, status=400)
        
        # Get recommendation from knowledge base
        recommendation = find_pesticide(crop, problem)
        pesticide_name = recommendation.get('pesticide', 'Unknown')
        
        # Log to blockchain asynchronously
        trigger_async_blockchain_log(
            type_name='pesticide',
            recommendation=pesticide_name,
            input_data={'crop': crop, 'problem': problem}
        )
        
        return Response({
            'status': 'success',
            'crop': crop,
            'problem_description': problem,
            'recommendation': recommendation
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['POST'])
def weather_tips(request):
    """
    Weather Based Farming Tips API
    Expects JSON: { "lat": 31.5204, "lon": 74.3587, "crop": "wheat" }
    """
    try:
        data = request.data
        
        lat = data.get('lat')
        lon = data.get('lon')
        crop = data.get('crop', None)
        
        if not lat or not lon:
            return Response({
                'status': 'error',
                'message': 'Missing fields: lat and lon (latitude, longitude)'
            }, status=400)
        
        # Get weather data
        weather = get_weather(lat, lon)
        
        if not weather:
            return Response({
                'status': 'error',
                'message': 'Unable to fetch weather data. Check your OpenWeatherMap API key.'
            }, status=500)
        
        # Get AI advice
        advice = get_farming_advice(weather, crop)
        
        # Log to blockchain asynchronously
        trigger_async_blockchain_log(
            type_name='weather',
            recommendation=f"Weather advice for {weather['location']}",
            input_data={'lat': lat, 'lon': lon, 'crop': crop}
        )
        
        return Response({
            'status': 'success',
            'location': weather['location'],
            'weather': {
                'temperature': weather['temperature'],
                'humidity': weather['humidity'],
                'conditions': weather['description'],
                'wind_speed': weather['wind_speed']
            },
            'farming_advice': advice
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)