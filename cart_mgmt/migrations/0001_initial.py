# Generated by Django 5.1 on 2024-10-15 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_console', '0003_user_last_updated'),
        ('product_mgmt', '0005_alter_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product_mgmt.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_console.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cart_mgmt.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_mgmt.product')),
            ],
        ),
    ]
