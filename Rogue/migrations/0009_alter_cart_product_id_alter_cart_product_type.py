# Generated by Django 5.1.5 on 2025-02-04 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rogue', '0008_remove_cart_product_cart_product_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_type',
            field=models.CharField(max_length=50),
        ),
    ]
