from django.urls import path
from .views import LoginUserView


urlpatterns = [
    path('user/', LoginUserView.as_view())
]
