# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 18:02
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('picture', models.FileField(default='shop/categories/images/no_image.png', upload_to='', verbose_name='Picture')),
                ('active', models.BooleanField(default=True, verbose_name='Is active')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=4, verbose_name='Rating')),
                ('review', models.TextField(default='Good')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('site', models.CharField(max_length=100, verbose_name='Site')),
                ('calculator_link', models.CharField(blank=True, max_length=150, verbose_name='Calculator')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('site', models.CharField(blank=True, max_length=150, verbose_name='Official Site')),
                ('short_description', models.TextField(blank=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Shopping is continued'), (2, 'Order created, but not processed'), (3, 'Order processed and waiting for assembly'), (4, 'Order assembled and wait for sent'), (5, 'Order was sent'), (6, 'Order delivered')], default=1, verbose_name='Status')),
                ('order_price', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Order price')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('ordered', models.DateTimeField(blank=True, verbose_name='Ordered')),
                ('tracking_number', models.CharField(blank=True, max_length=255, verbose_name='Tracking number')),
                ('total_weight', models.IntegerField(default=0, verbose_name='Weight')),
                ('total_size', models.CharField(blank=True, max_length=100, verbose_name='Size')),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Shipping cost')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Total cost')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('system_comment', models.TextField(blank=True, verbose_name='Working information')),
                ('delivery_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.DeliveryService')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='Count')),
                ('item_price', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Item cost')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('image', models.FileField(default='shop/products/images/no_image.png', upload_to='', verbose_name='Image')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='Added to stock')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('characteristics', django.contrib.postgres.fields.jsonb.JSONField(blank=True, verbose_name='Characteristics')),
                ('status', models.IntegerField(choices=[(1, 'Product in stock'), (2, 'Sorry, but product ended'), (3, 'Product is discontinued')], default=1, verbose_name='Status')),
                ('additional_status', models.IntegerField(choices=[(1, 'Novelty'), (2, 'Ends'), (3, 'Top of sales')], default=1, verbose_name='Additional status')),
                ('size', models.CharField(default='Unknown', max_length=100, verbose_name='Size')),
                ('weight', models.IntegerField(default=0, verbose_name='Weight')),
                ('total_count', models.IntegerField(default=0, verbose_name='Count')),
                ('discount', models.IntegerField(default=0, verbose_name='Discount')),
                ('product_code', models.CharField(blank=True, max_length=255, verbose_name='Product code')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Category', verbose_name='Category')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Manufacturer', verbose_name='Manufacturer')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Product'),
        ),
    ]