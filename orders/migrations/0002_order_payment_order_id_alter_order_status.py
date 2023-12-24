# Generated by Django 4.2.4 on 2023-12-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_order_id',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('process', 'Processing'), ('confirm', 'Confrimed'), ('ship', 'Shipped'), ('diliver', 'Delivered')], default='process', max_length=15),
        ),
    ]
