# Generated by Django 5.1 on 2024-10-23 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_console', '0003_user_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Suspended', 'Suspended'), ('Deactivated', 'Deactivated')], default='Active', max_length=20),
        ),
    ]
