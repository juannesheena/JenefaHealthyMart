# Generated by Django 3.0.4 on 2021-01-28 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_wallpaper_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallpaper',
            name='title',
            field=models.CharField(default=3, max_length=255),
            preserve_default=False,
        ),
    ]