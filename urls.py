# from django.urls import path
# from .views import get_weather

# urlpatterns = [
#     path("", get_weather, name="get_weather"),
# ]

# from django.urls import path
# from .views import get_weather, user_login, user_logout

# urlpatterns = [
#     path('', get_weather, name="get_weather"),  # Home (Weather App) - Requires login
#     path('login/', user_login, name="login"),   # Login Page
#     path('logout/', user_logout, name="logout"),  # Logout
# ]

from django.urls import path
from .views import weather_home, get_weather

urlpatterns = [
    path('', weather_home, name='home'),
    path('get_weather/', get_weather, name='get_weather'),
]
