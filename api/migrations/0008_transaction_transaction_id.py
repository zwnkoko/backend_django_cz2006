# Generated by Django 4.1.7 on 2023-03-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default='null', max_length=100),
        ),
    ]