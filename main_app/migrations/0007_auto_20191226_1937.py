# Generated by Django 3.0.1 on 2019-12-26 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20191226_1918'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Материал', 'verbose_name_plural': 'Материалы'},
        ),
        migrations.AlterModelOptions(
            name='materialapprovalrequest',
            options={'verbose_name': 'Запрос на публикацию', 'verbose_name_plural': 'Запросы на публикацию'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': 'Секция', 'verbose_name_plural': 'Секции'},
        ),
    ]
