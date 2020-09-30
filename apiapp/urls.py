from django.urls import path
import apiapp.views as apiapp

app_name = 'api'


urlpatterns = [
    path('registration/', apiapp.RegistrationUser.as_view(), name='registration'),
    path('authorization/', apiapp.AuthorizationUser.as_view(), name='authorization'),

    path('get_task_list/', apiapp.TaskList.as_view(), name='get_task_list'),
    path('create_task/', apiapp.TaskCreate.as_view(), name='create_task'),
]