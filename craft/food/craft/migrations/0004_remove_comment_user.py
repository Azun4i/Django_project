# Generated by Django 3.1 on 2020-09-10 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('craft', '0003_remove_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
    ]
