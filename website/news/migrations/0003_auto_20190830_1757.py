# Generated by Django 2.2.4 on 2019-08-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20190324_0006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsindex',
            old_name='introduction',
            new_name='summary',
        ),
        migrations.RemoveField(
            model_name='newspage',
            name='introduction',
        ),
        migrations.AddField(
            model_name='newspage',
            name='summary',
            field=models.TextField(blank=True, max_length=165, null=True),
        ),
    ]
