# Generated by Django 2.2 on 2020-05-19 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_userwork_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorinfomation',
            name='monitorimg',
            field=models.FileField(default='MonitorImg/default.png', null=True, upload_to='MonitorImg/', verbose_name='监控图片'),
        ),
    ]
