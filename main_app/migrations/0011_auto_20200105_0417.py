# Generated by Django 3.0.1 on 2020-01-05 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20200104_0311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['created_at'], 'verbose_name': 'Материал', 'verbose_name_plural': 'Материалы'},
        ),
        migrations.AddField(
            model_name='material',
            name='show_on_materials_page',
            field=models.BooleanField(default=False, verbose_name='Показывать на странице с материалами'),
        ),
    ]
