# Generated by Django 2.0.9 on 2019-03-16 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_personindexpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='personindexpage',
            name='introduction',
            field=models.TextField(blank=True),
        ),
    ]
