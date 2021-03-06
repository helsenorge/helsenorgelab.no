# Generated by Django 2.2.7 on 2019-12-16 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='information_url',
            field=models.URLField(blank=True, verbose_name='Mer informasjon'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='location_name',
            field=models.CharField(blank=True, max_length=250, verbose_name='Sted'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='program_url',
            field=models.URLField(blank=True, verbose_name='Program'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='streaming_url',
            field=models.URLField(blank=True, verbose_name='Direktestrømming'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='tickets_url',
            field=models.URLField(blank=True, verbose_name='Påmelding'),
        ),
    ]
