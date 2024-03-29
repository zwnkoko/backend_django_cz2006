# Generated by Django 4.1.7 on 2023-03-25 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.IntegerField()),
                ('receiver', models.IntegerField()),
                ('time', models.TimeField()),
                ('crypto_type', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
            ],
        ),
    ]
