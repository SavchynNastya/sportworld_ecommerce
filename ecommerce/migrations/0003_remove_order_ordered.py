# Generated by Django 4.1.2 on 2023-04-07 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_order_session_key_alter_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered',
        ),
    ]
