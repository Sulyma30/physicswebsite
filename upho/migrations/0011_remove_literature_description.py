# Generated by Django 3.1.1 on 2020-09-18 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upho', '0010_literature_literature_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='literature',
            name='description',
        ),
    ]
