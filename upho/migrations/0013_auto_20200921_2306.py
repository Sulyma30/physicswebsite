# Generated by Django 3.1.1 on 2020-09-21 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upho', '0012_auto_20200918_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='olympfile',
            name='pdf',
            field=models.FileField(upload_to='olympiads/'),
        ),
    ]