# Generated by Django 3.1 on 2020-09-25 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('craft', '0010_remove_cartproduct_final_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='user',
        ),
    ]
