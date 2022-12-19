# Generated by Django 4.1.2 on 2022-10-27 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=255)),
                ('message', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Места', 'verbose_name_plural': 'Места'},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['create_date', 'title'], 'verbose_name': 'Скидки', 'verbose_name_plural': 'Скидки'},
        ),
    ]