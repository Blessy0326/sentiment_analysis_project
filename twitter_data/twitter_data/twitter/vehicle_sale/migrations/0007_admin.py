# Generated by Django 3.2.5 on 2021-11-25 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_sale', '0006_auto_20211121_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Admin Name')),
                ('password', models.CharField(max_length=30, verbose_name='Password')),
            ],
        ),
    ]