# Generated by Django 2.2 on 2020-05-18 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_project_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.AddField(
            model_name='userlogin',
            name='avatar',
            field=models.FileField(default='avatars/default.png', null=True, upload_to='avatars/', verbose_name='头像'),
        ),
    ]
