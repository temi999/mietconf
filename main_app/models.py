from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    name = models.CharField(verbose_name='Название',
                            max_length=255,
                            unique=True)

    description = models.TextField(verbose_name='Описание')

    head = models.OneToOneField(User,
                                verbose_name='Руководитель секции',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Material(models.Model):
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    title = models.CharField(verbose_name='Заголовок',
                             max_length=75)

    description = models.TextField(verbose_name='Описание')

    content = models.TextField(verbose_name='Содержание')

    last_update = models.DateTimeField(verbose_name='Последнее обновление',
                                       auto_now=True)

    created_at = models.DateTimeField(verbose_name='Создан',
                                      auto_now_add=True)

    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE)

    section = models.ForeignKey(Section,
                                verbose_name='Секция',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - {0}'.format(self.section)


class MaterialApprovalRequest(models.Model):
    class Meta:
        verbose_name = 'Запрос на публикацию'
        verbose_name_plural = 'Запросы на публикацию'

    TECH = 'tech_sec'
    SCI = 'sci_sec'
    HEAD = 'head'

    ASSIGNED_TO_CHOICES = (
        (TECH, 'Техническому секретарю (Ожидает проверки оформления)'),
        (SCI, 'Учёному секретарю (Ожидает проверки на соответствие тематике)'),
        (HEAD, 'Руководителю секции (Ожидает подтверждения от руководителя секции)'),
    )

    material = models.OneToOneField(Material,
                                    verbose_name='Материал',
                                    on_delete=models.CASCADE)

    assigned_to = models.TextField(verbose_name='Назначен',
                                   choices=ASSIGNED_TO_CHOICES,
                                   max_length=255)

    last_update = models.DateTimeField(verbose_name='Последнее обновление',
                                       auto_now=True)

    created_at = models.DateTimeField(verbose_name='Создан',
                                      auto_now_add=True)

    def __str__(self):
        return self.material
