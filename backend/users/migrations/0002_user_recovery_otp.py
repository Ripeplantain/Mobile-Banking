# Generated by Django 4.1.4 on 2023-01-08 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='recovery_otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]