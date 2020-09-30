from django.urls import path
import apiapp.views as apiapp

app_name = 'api'


urlpatterns = [
    path('registration/', apiapp.RegistrationUser.as_view(), name='registration'),
    path('authorization/', apiapp.AuthorizationUser.as_view(), name='authorization'),
]