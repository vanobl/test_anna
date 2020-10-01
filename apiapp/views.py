import json
import string
import random
from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
# from django.db.models import Dose

from .models import Profile, Task



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


class TaskList(View):
    """
        Класс реализующий возврат пользователю списка его задач.

        Запрос на сервер осуществляется по шаблону:
        {
            'action': 'get_tasks_list',
            'filter_status': 'новая',
            'timeplane': ''
        }

        Ответ сервера осуществляется по шаблону:
        {
            'status': 'ok',
            'description': '',
            'total_tasks': 0,
            'tasks': [],
        }
    """
    def get(self, request, *args, **kwargs):
        json_str = get_json(self)

        token = self.request.META.get('HTTP_AUTHORIZATION')
        
        try:
            user = User.objects.get(profile__token=token)
            tasks = user.tasks.all()

            tasks_data = []

            for item in tasks:
                tasks_data.append(
                    {
                        'uuidtask':item.uuidtask,
                        'name':item.name
                    }
                )

            data = {
                'status': 'ok',
                'description': '',
                'total_tasks': tasks.count(),
                'tasks': tasks_data,
            }
        except User.DoesNotExist:
            data = {
                'status': 'error',
                'description': 'Пользователь не найден',
                'total_tasks': 0,
                'tasks': {}
            }
        except Exception as ex:
            data = {
                'status': 'error',
                'description': f'Ошибка: {ex.__class__}',
                'total_tasks': 0,
                'tasks': {}
            }
    
        return JsonResponse(
            data,
            json_dumps_params={"ensure_ascii": False}
        )


class TaskCreate(View):
    """
        Класс реализующий создание задачи.

        Запрос на сервер осуществляется по шаблону:
        {
            'action': 'create_task',
            'task': {
                'name': 'пробная',
                'description': '',
                'timeplane': '2020-10-25',
            }
        }

        Ответ сервера осуществляется по шаблону:
        {
            'status': 'error',
            'description': '',
            'total_tasks': 0,
            'tasks': {}
        }
    """
    def get(self, request, *args, **kwargs):
        json_str = get_json(self)

        token = self.request.META.get('HTTP_AUTHORIZATION')

        try:
            user = User.objects.get(profile__token=token)
        except User.DoesNotExist:
            data = {
                'status': 'error',
                'description': 'Пользователь не найден',
                'total_tasks': 0,
                'tasks': {}
            }
        
        try:
            task = Task(
                user=user,
                name=json_str['task']['name'],
                description=json_str['task']['description'],
                timeplane=datetime.strptime(json_str['task']['timeplane'], '%Y-%m-%d'),
                status=1
            )
            task.save()
            data = {
                'status': 'ok',
                'description': 'Задание успешно сохранено.',
                'uuid_tasks': task.uuidtask,
            }
        except KeyError as ex:
            data = {
                'status': 'error',
                'description': f'Ошибка: {ex.__class__}. Отсутствует поле {ex}',
            }


        return JsonResponse(
            data,
            json_dumps_params={"ensure_ascii": False}
        )