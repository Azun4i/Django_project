# Generated by Django 3.1 on 2020-09-25 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('craft', '0009_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='final_price',
        ),
    ]
