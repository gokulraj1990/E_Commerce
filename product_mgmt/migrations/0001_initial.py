# Generated by Django 5.1 on 2024-09-21 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productID', models.CharField(editable=False, max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('category', models.CharField(choices=[('ELEC', 'Electronics'), ('FASH', 'Fashion'), ('TOYS', 'Toys')], max_length=20)),
                ('imageUrl', models.URLField(blank=True)),
            ],
        ),
    ]