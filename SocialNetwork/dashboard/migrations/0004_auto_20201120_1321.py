# Generated by Django 3.0.8 on 2020-11-20 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20201120_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(default='images/user.jpg', null=True, upload_to='documents/'),
        ),
    ]
