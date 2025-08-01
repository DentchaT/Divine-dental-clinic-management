# Generated by Django 5.2.4 on 2025-07-29 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divine_dental_clinic', '0004_alter_leaveapplication_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
