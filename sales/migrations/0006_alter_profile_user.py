# Generated by Django 4.1.2 on 2022-11-07 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_profile_user_alter_profile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.CharField(max_length=30),
        ),
    ]
