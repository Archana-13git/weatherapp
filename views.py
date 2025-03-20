# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# import requests
# from .models import Weather

# API_KEY = "b0e8a76a9f46c27c2b418ebfbce1d033"

# # ✅ Ensure users must log in every time before accessing the weather app
# @login_required(login_url='/login/')
# def get_weather(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
#         if not city:
#             return JsonResponse({"error": "City not provided"}, status=400)

#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#         response = requests.get(url).json()

#         if response.get("main"):
#             weather = Weather.objects.create(
#                 city=city,
#                 temperature=response["main"]["temp"],
#                 humidity=response["main"]["humidity"],
#                 description=response["weather"][0]["description"]
#             )
#             weather.save()

#             return JsonResponse({"weather": {
#                 "city": weather.city,
#                 "temperature": weather.temperature,
#                 "humidity": weather.humidity,
#                 "description": weather.description
#             }})
#         else:
#             return JsonResponse({"error": "City not found"}, status=404)

#     return render(request, "weather_app/weather.html")

# # ✅ Fix Login View to Work Every Time
# def user_login(request):
#     if request.user.is_authenticated:
#         return redirect('/')  # If already logged in, go to the weather page

#     if request.method == "POST":
#         username = request.POST.get("username")  
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#             request.session.set_expiry(0)  # 🔥 Ensure login expires when the browser is closed
#             return redirect('/')  # Redirect to weather page after login
#         else:
#             return render(request, "weather_app/login.html", {"error": "Invalid username or password"})

#     return render(request, "weather_app/login.html")

# # ✅ Fix Logout to Redirect to Login Every Time
# def user_logout(request):
#     logout(request)
#     return redirect('/login/')  # Redirect to login page after logout


import requests
from django.shortcuts import render
from django.http import JsonResponse

API_KEY = "b0e8a76a9f46c27c2b418ebfbce1d033"

def weather_home(request):
    return render(request, "weather_app/weather.html")

def get_weather(request):
    """Fetch weather data using AJAX and return JSON response."""
    if request.method == "GET":
        city = request.GET.get("city")
        if not city:
            return JsonResponse({"error": "City not provided"}, status=400)

        # Fetch Current Weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        weather_response = requests.get(weather_url).json()

        # Fetch 5-Day Forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url).json()

        if weather_response.get("cod") != 200 or forecast_response.get("cod") != "200":
            return JsonResponse({"error": "City not found"}, status=404)

        # Extract necessary data
        weather_data = {
            "city": weather_response["name"],
            "temperature": weather_response["main"]["temp"],
            "humidity": weather_response["main"]["humidity"],
            "description": weather_response["weather"][0]["description"].capitalize(),
            "icon": weather_response["weather"][0]["icon"],
            "forecast": []
        }

        # Extract 5-day forecast (every 24 hours)
        for i in range(0, 40, 8):  # Every 8th item (24-hour gap)
            day_forecast = forecast_response["list"][i]
            weather_data["forecast"].append({
                "date": day_forecast["dt_txt"].split()[0],
                "temperature": day_forecast["main"]["temp"],
                "description": day_forecast["weather"][0]["description"].capitalize(),
                "icon": day_forecast["weather"][0]["icon"]
            })

        return JsonResponse(weather_data)

    return JsonResponse({"error": "Invalid request"}, status=400)
