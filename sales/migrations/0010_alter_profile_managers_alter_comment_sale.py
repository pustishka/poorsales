# Generated by Django 4.1.2 on 2022-11-18 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_comment'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='sale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='sales.sale'),
        ),
    ]
