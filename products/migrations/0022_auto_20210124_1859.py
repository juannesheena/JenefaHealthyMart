# Generated by Django 3.0.4 on 2021-01-24 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20210124_1848'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TrendingProducts',
            new_name='TrendingProduct',
        ),
    ]
