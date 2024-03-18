import datetime

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Кто получает рассылку"""
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    surname = models.CharField(max_length=100, **NULLABLE, verbose_name='Отчество')
    email = models.EmailField(unique=True, verbose_name='Почта')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name', 'first_name',)


class Message(models.Model):
    """Сообщение рассылки"""
    title = models.CharField(max_length=150, default='Без темы', verbose_name='Тема письма')
    text_body = models.TextField(**NULLABLE, verbose_name='Содержание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('title',)


class Mailing(models.Model):
    """Настройки и статусы рассылки"""
    PERIOD_CHOICES = (
        ('once', '1 раз'),
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('stopped', 'Завершена'),
    )

    title = models.CharField(max_length=150, verbose_name='Название рассылки')

    date_start = models.DateTimeField(default=datetime.datetime.now, verbose_name='Время начала рассылки')
    date_stop = models.DateTimeField(default=datetime.datetime.now, verbose_name='Время окончания рассылки')
    period = models.CharField(choices=PERIOD_CHOICES, default='once', verbose_name='Периодичность рассылки')
    status = models.CharField(choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')

    client = models.ManyToManyField(Client, verbose_name='Получатели')
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name='Сообщение')

    is_active = models.BooleanField(default=True, verbose_name='Активная')

    def __str__(self):
        return f' {self.title} ({self.date_start}-{self.date_stop}, {self.period}, {self.status})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('status',)


class Logs(models.Model):
    """Логи и статусы логов рассылки"""
    LOG_CHOICES = (
        (True, 'Успешно'),
        (False, 'Ошибка'),
    )

    attempt_time = models.DateTimeField(verbose_name='Дата и время последней попытки', **NULLABLE)
    attempt_status = models.CharField(max_length=50, choices=LOG_CHOICES, default=True, verbose_name='Статус попытки')
    server_response = models.CharField(max_length=255, verbose_name='Ответ почтового сервера', **NULLABLE)

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент рассылки', **NULLABLE)

    def __str__(self):
        return f'Попытка отправки {self.attempt_time}, статус - {self.attempt_status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('attempt_status',)
