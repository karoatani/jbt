# Generated by Django 4.2.7 on 2023-11-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_tracking_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_key', models.CharField(max_length=255)),
                ('otp', models.IntegerField()),
                ('exp_date', models.DateTimeField()),
            ],
        ),
    ]