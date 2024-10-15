
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-login/', auth_views.LoginView.as_view(), name='my_login'),
    path('', include('journal.urls')),
]















