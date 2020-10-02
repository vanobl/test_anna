import json
import string
import random
from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
# from django.db.models import Dose

from .models import Profile, Task, HistoryChangeTask



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
            'filter_timeplane_start': '',
            'filter_timeplane_end': ''
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

            if json_str['action'] == 'get_tasks_list':
                if json_str['filter_timeplane_start'] and json_str['filter_timeplane_end']:
                    tasks = user.tasks.filter(status=json_str['filter_status']).filter(
                        timeplane__range=(
                            datetime.strptime(json_str['filter_timeplane_start'], '%Y-%m-%d'),
                            datetime.strptime(json_str['filter_timeplane_end'], '%Y-%m-%d')
                        )
                    )
                else:
                    tasks = user.tasks.filter(status=json_str['filter_status'])

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
            else:
                data = {
                'status': 'error',
                'description': f'Ошибка! Не допустимое значение action: {json_str["action"]}',
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

            if json_str['action'] == 'create_task':
                task = Task(
                    user=user,
                    name=json_str['task']['name'],
                    description=json_str['task']['description'],
                    timeplane=datetime.strptime(json_str['task']['timeplane'], '%Y-%m-%d %H:%M'),
                    status=1
                )
                task.save()
                history_task = HistoryChangeTask(task=task, name=task.name, description=task.description, timeplane=task.timeplane, status=task.status)
                history_task.save()
                data = {
                    'status': 'ok',
                    'description': 'Задание успешно сохранено.',
                    'uuid_tasks': task.uuidtask,
                }
            else:
                data = {
                'status': 'error',
                'description': f'Ошибка! Не допустимое значение action: {json_str["action"]}',
                }
        except User.DoesNotExist:
            data = {
                'status': 'error',
                'description': 'Пользователь не найден',
                'total_tasks': 0,
                'tasks': {}
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


class TaskInfo(View):
    """
        Класс реализующий получение информации по конкретной задаче.

        Запрос на сервер осуществляется по шаблону:
        {
            'action': 'info_task',
            'uuid_task': ''
        }

        Ответ сервера осуществляется по шаблону:
         {
            'status': 'ok',
            'description': '',
            'tasks': {
                'name': '',
                'description': '',
                'timecreate': '',
                'status': '',
                'timeplane': ''
            }
        }

        поле 'status' может принимать значения 'ok' или 'error'

        поле 'tasks' будет включено в файл, если поле 'status' иммет значение 'ok'
    """
    def get(self, request, *args, **kwargs):
        json_str = get_json(self)

        token = self.request.META.get('HTTP_AUTHORIZATION')

        try:
            user = User.objects.get(profile__token=token)

            if json_str['action'] == 'info_task':
                my_task = Task.objects.get(uuidtask=json_str['uuid_task'])

                data = {
                    'status': 'ok',
                    'description': 'Задание успешно получено.',
                    'tasks': {
                        'name': my_task.name,
                        'description': my_task.description,
                        'timecreate': my_task.timecreate,
                        'status': my_task.status,
                        'timeplane': my_task.timeplane
                    }
                }
            else:
                data = {
                'status': 'error',
                'description': f'Ошибка! Не допустимое значение action: {json_str["action"]}',
            }
        except User.DoesNotExist:
            data = {
                'status': 'error',
                'description': 'Пользователь не найден',
            }
        except KeyError as ex:
            data = {
                'status': 'error',
                'description': f'Ошибка: {ex.__class__}. Отсутствует поле {ex}',
            }
        except Exception as ex:
            data = {
                'status': 'error',
                'description': f'Ошибка: {ex.__class__}.',
            }
        
        return JsonResponse(
            data,
            json_dumps_params={"ensure_ascii": False}
        )


class TaskChange(View):
    """
        Класс реализующий изменение данных задачи

        Запрос на сервер осуществляется по шаблону:
        {
            'action': 'change_task',
            'uuid_task': '',
            'task': {
                'name': '',
                'description': '',
                'timeplane': '2020-12-30 23:59',
                'status': 4
            }
        }

        Ответ сервера осуществляется по шаблону:
        {
            'status': 'ok',
            'description': 'Задание успешно изменено.',
            'tasks': {
                'name': '',
                'description': '',
                'status': '',
                'timeplane': ''
            }
        }

        поле 'status' может принимать значения 'ok' или 'error'

        поле 'tasks' включается в файл, если поле 'status' имеет значение 'ok'
    """
    def get(self, request, *args, **kwargs):
        json_str = get_json(self)

        token = self.request.META.get('HTTP_AUTHORIZATION')

        try:
            user = User.objects.get(profile__token=token)

            if json_str['action'] == 'change_task':
                my_task = Task.objects.get(uuidtask=json_str['uuid_task'], user=user)

                if 'name' in json_str['task']:
                    my_task.name = json_str['task']['name']

                if 'description' in json_str['task']:
                    my_task.description = json_str['task']['description']

                if 'status' in json_str['task']:
                    my_task.status = json_str['task']['status']

                if 'timeplane' in json_str['task']:
                    my_task.timeplane = datetime.strptime(json_str['task']['timeplane'], '%Y-%m-%d %H:%M')
                
                my_task.save()

                history_task = HistoryChangeTask(task=my_task, name=my_task.name, description=my_task.description, timeplane=my_task.timeplane, status=my_task.status)
                history_task.save()

                data = {
                    'status': 'ok',
                    'description': 'Задание успешно изменено.',
                    'tasks': {
                        'name': my_task.name,
                        'description': my_task.description,
                        'status': my_task.status,
                        'timeplane': my_task.timeplane
                    }
                }
            else:
                data = {
                'status': 'error',
                'description': f'Ошибка! Не допустимое значение action: {json_str["action"]}',
                }
        except User.DoesNotExist:
            data = {
                'status': 'error',
                'description': 'Пользователь не найден',
            }
        except Task.DoesNotExist:
            data = {
                'status': 'error',
                'description': 'Задача не найдена',
            }
        except KeyError as ex:
            data = {
                'status': 'error',
                'description': f'Ошибка: {ex.__class__}. Отсутствует поле {ex}',
            }
        except Exception as ex:
            data = {
                'status': 'error',
                'description': f'Ошибка: {ex.__class__}.',
            }
        
        return JsonResponse(
            data,
            json_dumps_params={"ensure_ascii": False}
        )