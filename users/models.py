from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from main_app.models import Section

MAIN_SECTION_NAME = 'Нет секции'


class UserProfile(models.Model):
    """ Расширяет базовую модель пользователя, при помощи связи 1 к 1
    status, profile pic, birth date, location"""

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    STATUS_CHOICES = (
        ('participant', 'Участник'),
        ('approving', 'Ожидает получения статуса автора'),
        ('author', 'Автор'),
        ('tech_sec', 'Технический секретарь'),
        ('sci_sec', 'Учёный секретарь'),
        ('head', 'Руководитель секции'),
    )

    user = models.OneToOneField(User,
                                verbose_name='Пользователь',
                                on_delete=models.CASCADE)

    location = models.CharField(verbose_name='Местоположение',
                                max_length=50, blank=True)

    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)

    status = models.CharField(verbose_name='Статус',
                              choices=STATUS_CHOICES,
                              max_length=255)

    section = models.ForeignKey(Section,
                                verbose_name='Секция',
                                on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, location='', birth_date=None,
                                   status='participant', section=Section.objects.get(name=MAIN_SECTION_NAME))


class AuthorApprovalRequest(models.Model):
    class Meta:
        verbose_name = 'Запрос статуса автора'
        verbose_name_plural = 'Запросы статуса автора'

    author = models.OneToOneField(User,
                                  verbose_name='Автор',
                                  on_delete=models.CASCADE)

    cover_letter = models.TextField(verbose_name='Сопроводительное письмо')

    section = models.OneToOneField(Section,
                                   verbose_name='Секция',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username
