from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from main_app.models import Section, Material

MAIN_SECTION_NAME = 'Нет секции'


class UserProfile(models.Model):
    """ Расширяет базовую модель пользователя, при помощи связи 1 к 1
    status,  birth date, location"""

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    PART = 'participant'
    AUTHOR = 'author'
    APPROVING = 'approving'
    TECH = 'tech_sec'
    SCI = 'sci_sec'
    HEAD = 'head'

    STATUS_CHOICES = (
        (PART, 'Участник'),
        (APPROVING, 'Ожидает получения статуса автора'),
        (AUTHOR, 'Автор'),
        (TECH, 'Технический секретарь'),
        (SCI, 'Учёный секретарь'),
        (HEAD, 'Руководитель секции'),
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

    def is_staff(self):
        return self.status in ('tech_sec', 'sci_sec', 'head')

    def is_author(self):
        return self.status == 'author'

    def profile_name(self):
        addition = ''
        if self.user.first_name and not self.user.last_name:
            addition += f' ({self.user.first_name})'
        elif self.user.first_name and self.user.last_name:
            addition += f' ({self.user.first_name} {self.user.last_name})'
        return self.user.username + addition

    def is_profile_set(self):
        return self.user.first_name and self.user.last_name and self.user.email \
               and self.location and self.birth_date

    def is_request_allowed(self):
        if AuthorApprovalRequest.objects.filter(author=self.user).exists():
            return False

        if not self.status == self.PART:
            return False

        return True

    def can_send_material(self):
        if Material.objects.filter(author=self.user).exists():
            return False
        return True

    def change_status(self, new_status):
        self.status = new_status
        if AuthorApprovalRequest.objects.filter(author=self.user).exists():
            AuthorApprovalRequest.objects.get(author=self.user).delete()
        self.save()


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

    section = models.ForeignKey(Section,
                                verbose_name='Секция',
                                on_delete=models.CASCADE)

    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return self.author.username

    def consider(self, accept: bool):
        if accept:
            self.author.userprofile.status = 'author'
        else:
            self.author.userprofile.status = 'participant'
        self.author.userprofile.save()
        self.delete()
