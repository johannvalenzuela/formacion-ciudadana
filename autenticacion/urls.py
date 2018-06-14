from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('politica_privacidad/', views.PoliticaPrivacidad.as_view(), name='politica_privacidad'),
    path('login_success/', views.login_success, name='login_success'),
    
]