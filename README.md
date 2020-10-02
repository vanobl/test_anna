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

Для запуска проекта возможно потребуется сбросить миграции
```
python manage.py migrate app zero --fake
```
