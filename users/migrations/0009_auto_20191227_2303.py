# Generated by Django 3.0.1 on 2019-12-27 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20191226_1937'),
        ('users', '0008_auto_20191226_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorapprovalrequest',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Section', verbose_name='Секция'),
        ),
    ]
