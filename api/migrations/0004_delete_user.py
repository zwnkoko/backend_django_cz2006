# Generated by Django 4.1.7 on 2023-03-25 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]