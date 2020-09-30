import json
import string
import random
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User, auth
from django.http import JsonResponse

from .models import Profile



# генератор токена для организации
def randomtoken():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    size=1
    mytxt = ''

    for _ in range(size,32):
        mytxt = mytxt + random.choice(chars)
    
    token = mytxt.strip()
    return token

def get_json(myself):
    body_str = myself.request.body.decode('utf-8')
    json_str = json.loads(body_str)
    return json_str


# регистрация пользователя
class RegistrationUser(View):
    """
        Класс реализующий механизм регистрации пользователя.

        Запрос на сервер осуществляется по шаблону:
        {
            'action': 'create',
            'user': {
                'username': '',
                'password': ''
            }
        }

        Ответ сервера осуществляется по шаблону:
        {
            'status': 'ok',
            'description': ''
        }, где "status" - принимает значения "ok" или "error";
        "description" - описание статуса
    """
    def get(self, request, *args, **kwargs):
        json_str = get_json(self)

        new_user, created_user = User.objects.get_or_create(
            username=json_str['user']['username'],
        )

        if created_user:
            new_user.set_password(json_str['user']['password'])
            new_user.save()
            this_token = randomtoken()
            profile = Profile(user=new_user, token=this_token)
            profile.save()
            return JsonResponse(
                {
                    'status': 'ok',
                    'description': 'Пользователь успешно создан',
                },
                json_dumps_params={"ensure_ascii": False}
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'description': 'Указанное имя пользователя уже занято. Пользователь не создан.',
                },
                json_dumps_params={"ensure_ascii": False}
            )


class AuthorizationUser(View):
    """
        Класс реализующий механизм авторизации пользователя.

        Запрос на сервер осуществляется по шаблону:
        {
            'action': '',
            'user': {
                'username': '',
                'password': ''
            }
        }

        Ответ сервера осуществляется по шаблону:
        {
            'status': '',
            'description': '',
            'token': ''
        }, где "status" - принимает значения "ok" или "error";
        "description" - описание статуса;
        "token" - строка, если "status" имеет значение "ok"
    """
    def get(self, request, *args, **kwargs):
        json_str = get_json(self)

        user = auth.authenticate(
            username=json_str['user']['username'],
            password=json_str['user']['password']
        )
        
        if user:
            return JsonResponse(
                {
                    'status': 'ok',
                    'description': 'Пользователь успешно авторизировался.',
                    'token': user.profile.token
                },
                json_dumps_params={"ensure_ascii": False}
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'description': 'Логин или пароль не верен.',
                },
                json_dumps_params={"ensure_ascii": False}
            )