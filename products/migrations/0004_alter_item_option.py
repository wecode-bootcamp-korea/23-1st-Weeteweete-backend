# Generated by Django 3.2.6 on 2021-08-11 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_item_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.option'),
        ),
    ]
