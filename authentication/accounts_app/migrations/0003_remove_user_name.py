# Generated by Django 3.2.5 on 2021-07-15 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0002_auto_20210714_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
