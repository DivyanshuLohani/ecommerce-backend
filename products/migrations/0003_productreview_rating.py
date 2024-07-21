# Generated by Django 4.2.4 on 2023-10-17 14:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='rating',
            field=models.PositiveIntegerField(default=1, error_messages=['The rating should be between 1 and 10'], validators=[django.core.validators.MaxValueValidator(10)]),
            preserve_default=False,
        ),
    ]
