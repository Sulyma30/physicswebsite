# Generated by Django 3.1.1 on 2020-09-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='full_title',
            field=models.CharField(default='ok', max_length=200),
            preserve_default=False,
        ),
    ]