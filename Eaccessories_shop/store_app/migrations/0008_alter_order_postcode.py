# Generated by Django 4.2 on 2023-04-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0007_remove_order_additional_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='postcode',
            field=models.IntegerField(max_length=50),
        ),
    ]
