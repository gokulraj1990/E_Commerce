# Generated by Django 5.1 on 2024-10-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_console', '0004_alter_user_firstname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
