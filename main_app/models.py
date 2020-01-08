from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def upload_path(instance, filename):
    return '{0}/{1}/{2}/{3}'.format(instance.section.name,
                                     instance.author.username,
                                     instance.title,
                                     filename)


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
        ordering = ['created_at']

    TECH = 'tech_sec'
    SCI = 'sci_sec'
    HEAD = 'head'
    APPROVED = 'approved'

    STATUS_CHOICES = (
        (TECH, 'Проверка оформления'),
        (SCI, 'Проверка тезисов'),
        (HEAD, 'Ожидает подтверждения'),
        (APPROVED, 'Материал подтвержден')
    )

    title = models.CharField(verbose_name='Заголовок',
                             max_length=75)

    description = models.TextField(verbose_name='Описание')

    document = models.FileField(upload_to=upload_path,
                                verbose_name='Документ',
                                null=True)

    presentation = models.FileField(upload_to=upload_path,
                                    verbose_name='Презентация',
                                    null=True)

    status = models.CharField(verbose_name='Статус',
                              choices=STATUS_CHOICES,
                              max_length=255)

    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE)

    section = models.ForeignKey(Section,
                                verbose_name='Секция',
                                on_delete=models.CASCADE)

    show_on_materials_page = models.BooleanField(verbose_name='Показывать на странице с материалами',
                                                 default=False)

    last_update = models.DateTimeField(verbose_name='Последнее обновление',
                                       auto_now=True)

    created_at = models.DateTimeField(verbose_name='Создан',
                                      auto_now_add=True)

    def __str__(self):
        return self.title + ' - {0}'.format(self.section.name)

    def consider(self, accept:bool):
        if accept:
            if self.status == self.TECH:
                self.status = self.SCI
            elif self.status == self.SCI:
                self.status = self.HEAD
            elif self.status == self.HEAD:
                self.status = self.APPROVED
            self.save()
        else:
            self.delete()

    def material_page_set(self):
        return self.objects.filter(show_on_materials_page=True)

@receiver(post_delete, sender=Material)
def submission_delete(sender, instance, **kwargs):
    """ При удалении материала удалить связанные с ним файлы """
    instance.document.delete(False)
    instance.presentation.delete(False)
