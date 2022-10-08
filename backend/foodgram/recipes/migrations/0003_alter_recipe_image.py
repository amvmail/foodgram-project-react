# Generated by Django 3.2.4 on 2022-10-08 14:54

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_amount_quantity_gte_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='recipes/', validators=[recipes.validators.image_size_validator], verbose_name='изображение'),
        ),
    ]