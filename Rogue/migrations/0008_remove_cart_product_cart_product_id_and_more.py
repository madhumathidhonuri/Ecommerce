# Generated by Django 5.1.5 on 2025-02-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rogue', '0007_footwear_color_alter_cargos_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.AddField(
            model_name='cart',
            name='product_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cart',
            name='product_type',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
