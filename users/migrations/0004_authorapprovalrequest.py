# Generated by Django 3.0.1 on 2019-12-26 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0004_delete_authorapprovalrequest'),
        ('users', '0003_auto_20191226_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorApprovalRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField()),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('section', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.Section')),
            ],
        ),
    ]
