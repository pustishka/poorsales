# Generated by Django 4.1.2 on 2022-12-09 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0017_alter_sale_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='duration',
            field=models.DateField(blank=True, null=True),
        ),
    ]
