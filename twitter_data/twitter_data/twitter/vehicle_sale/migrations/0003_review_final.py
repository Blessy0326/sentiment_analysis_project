# Generated by Django 3.2.4 on 2021-11-21 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_sale', '0002_auto_20211121_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review_final',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=30, verbose_name='Review')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='vehicle_sale.product')),
            ],
        ),
    ]
