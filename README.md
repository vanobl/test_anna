# API для ведения своих задач

В проекте реализованы следующие функции:
1. Регистрация пользователя в системе;
2. Авторизация пользователя в системе с получением токена для клиента;
3. Получение клиентом списка своих задач;
4. Получение детальной информации по задаче;
5. Изменение информации задачи;
6. Логирование изменений по задаче.

### Технологии

Проект написан на Python с использованием фреймворка Django.

### Запуск проекта

Для запуска проекта возможно потребуется сбросить миграции. Для этого переходим в папку с проектом, и выполняем в терминале:
```
python manage.py migrate apiapp zero --fake
python manage.py makemigrations apiapp
python manage.py migrate
```

В папке \"client\" лежит файл \"test_anna.py\". В нём подготовлены ссылки, используемые в проекте:
```
REGISTRATION = 'http://127.0.0.1:8000/api/registration/'
AUTHORIZATION = 'http://127.0.0.1:8000/api/authorization/'
TASK_LIST = 'http://127.0.0.1:8000/api/get_task_list/'
TASK_CREATE = 'http://127.0.0.1:8000/api/create_task/'
TASK_INFO = 'http://127.0.0.1:8000/api/info_task/'
TASK_CHANGE = 'http://127.0.0.1:8000/api/change_task/'
```

Так же подготовлены данные для отправки на в проект в формате JSON:
* my_data_registration
* my_data_authenticate
* my_data_get_task_list
* my_data_create_task
* my_data_info_task
* my_data_change_task

Подставляя соответствующие данные в переменные \"jdata\" и \"url\" можно выполнять запросы на сервер
```
jdata = json.dumps(my_data_get_task_list)

url = TASK_LIST
```
