# Generated by Django 4.1.7 on 2023-03-28 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_transaction_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='crypto_type',
            new_name='crypto',
        ),
    ]