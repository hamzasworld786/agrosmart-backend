import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def get_weather(lat, lon):
    """Get real weather data from OpenWeatherMap"""
    if OPENWEATHER_API_KEY:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'pressure': data['main']['pressure'],
                    'location': data.get('name', 'Your Area'),
                    'source': 'OpenWeatherMap'
                }
        except Exception as e:
            print(f"Weather API error: {e}")
    
    # Fallback mock data
    return {
        'temperature': 30.0,
        'humidity': 50,
        'description': 'clear sky',
        'wind_speed': 2.0,
        'pressure': 1012,
        'location': 'Islamabad',
        'source': 'Mock'
    }

def get_farming_advice(weather_data, crop_type=None):
    """Generate farming advice - uses fallback when API quota exceeded"""
    
    temp = weather_data['temperature']
    humidity = weather_data['humidity']
    conditions = weather_data['description'].lower()
    location = weather_data['location']
    
    # Try Gemini first if available, but don't rely on it
    if GEMINI_API_KEY:
        try:
            # Try to import and use Gemini
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('models/gemini-2.0-flash')
            
            prompt = f"""You are an agricultural expert advising a farmer in {location} growing {crop_type or 'crops'}.

Weather: {temp}°C, {humidity}% humidity, {conditions}, wind {weather_data['wind_speed']} m/s.

Give VERY SHORT advice in EXACT format:
💧 WATERING: (Yes/No) - (4-5 words reason)
🌱 FERTILIZER: (Good/Wait) - (4-5 words reason)
🐛 PEST RISK: (Low/Medium/High) - (3-4 words)
✅ TIP: (one 5-8 word sentence)"""

            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Gemini error (using fallback): {e}")
            # Fall through to fallback
    
    # FALLBACK ADVICE - Always works, no API calls needed
    return get_fallback_advice(weather_data, crop_type)

def get_fallback_advice(weather_data, crop_type=None):
    """Return pre-written advice - reliable for demo"""
    temp = weather_data['temperature']
    humidity = weather_data['humidity']
    conditions = weather_data['description'].lower()
    
    # Smart rule-based advice
    if "rain" in conditions:
        watering = "No - Rain provides moisture"
        fertilizer = "Wait - Rain may wash away"
        pest = "Medium - Check for fungus"
        tip = "Cover sensitive crops from heavy rain"
    elif "thunderstorm" in conditions:
        watering = "No - Storm coming"
        fertilizer = "Wait - Unsafe conditions"
        pest = "Low - Wind disrupts pests"
        tip = "Secure loose plants and shelters"
    elif temp > 38:
        watering = "Yes - Extreme heat! Water deeply"
        fertilizer = "Wait - Heat causes burn"
        pest = "High - Watch for mites"
        tip = "Provide shade for young plants"
    elif temp > 32:
        watering = "Yes - Hot day, water early morning"
        fertilizer = "Good - Apply diluted"
        pest = "Medium - Check for aphids"
        tip = "Mulch to retain moisture"
    elif temp < 15:
        watering = "No - Cold, reduce watering"
        fertilizer = "Wait - Cold reduces uptake"
        pest = "Low - Cold slows pests"
        tip = "Protect from frost if needed"
    elif humidity > 80:
        watering = "No - High humidity"
        fertilizer = "Wait - Risk of fungal growth"
        pest = "High - Fungal disease risk"
        tip = "Ensure good air circulation"
    elif humidity < 30:
        watering = "Yes - Very dry conditions"
        fertilizer = "Good - Water before applying"
        pest = "Medium - Check for spider mites"
        tip = "Increase watering frequency"
    else:
        watering = "Check - Moderate conditions"
        fertilizer = "Good time to apply"
        pest = "Low - Conditions favorable"
        tip = "Regular monitoring recommended"
    
    # Add crop-specific tips
    crop_tip = ""
    if crop_type:
        crop_lower = crop_type.lower()
        if crop_lower in ["rice", "paddy"]:
            crop_tip = f" For rice, maintain 2-3cm water level."
        elif crop_lower in ["wheat", "gehu"]:
            crop_tip = f" For wheat, avoid water logging."
        elif crop_lower in ["maize", "corn", "makai"]:
            crop_tip = f" For maize, ensure proper spacing."
        elif crop_lower in ["cotton", "kapas"]:
            crop_tip = f" For cotton, watch for bollworms."
    
    return f"""🌾 WEATHER BASED FARMING ADVICE
📍 Location: {weather_data['location']}
🌡️ {temp}°C | 💧 {humidity}% | 🌬️ {weather_data['wind_speed']} m/s
{'🌱 Crop: ' + crop_type if crop_type else ''}

💧 WATERING: {watering}

🌱 FERTILIZER: {fertilizer}

🐛 PEST RISK: {pest}

✅ TODAY'S TIP: {tip}{crop_tip}

---
💡 Tip: Connect to internet for AI-powered advice!"""