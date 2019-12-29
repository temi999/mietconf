# Generated by Django 3.0.1 on 2019-12-26 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_authorapprovalrequest'),
        ('users', '0002_auto_20191226_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Section'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(max_length=50),
        ),
    ]