# Generated by Django 5.1 on 2024-10-03 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_mgmt', '0002_rename_model_product_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Kitchen Appliances', 'Kitchen Appliances'), ('Home Appliances', 'Home Appliances'), ('Entertainment', 'Entertainment'), ('Books', 'Books')], max_length=20),
        ),
    ]
