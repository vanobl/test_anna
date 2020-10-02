import uuid
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    """
        Таблица для профиля пользователя, в котором хранится токен для api.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',)
    token = models.CharField(verbose_name='токен', max_length=32, blank=False, unique=True, null=False)


class Task(models.Model):
    """
        Таблица для хранения задач пользователей.
        Поле 'status' может принимать значения:
            1 - новая
            2 - запланированная
            3 - в работе
            4 - завершённая
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks',)
    name = models.CharField(verbose_name='название', max_length=128, blank=False, null=False)
    description = models.TextField(verbose_name='описание')
    timecreate = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    timeupdate = models.DateTimeField(verbose_name='время последнего изменения', auto_now=True)
    status = models.PositiveIntegerField(verbose_name='статус')
    timeplane = models.DateTimeField(verbose_name='планируемое время завершения')
    uuidtask = models.UUIDField(verbose_name='уникальный идентификатор', default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.name} - {self.uuidtask}'


class HistoryChangeTask(models.Model):
    """
        Таблица для хранения истории создания и изменения задач
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    name = models.CharField(verbose_name='название', max_length=128, blank=False, null=False)
    description = models.TextField(verbose_name='описание')
    timecreate = models.DateTimeField(verbose_name='время создания истороии', auto_now_add=True)
    status = models.PositiveIntegerField(verbose_name='статус')
    timeplane = models.DateTimeField(verbose_name='планируемое время завершения')

    def __str__(self):
        return f'{self.name}'