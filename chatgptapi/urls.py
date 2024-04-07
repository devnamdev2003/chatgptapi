from django.urls import path
from api import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_input, name='user_input'),
]
