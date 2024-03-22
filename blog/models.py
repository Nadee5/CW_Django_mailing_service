from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    publication_date = models.DateField(auto_now=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('publication_date',)
