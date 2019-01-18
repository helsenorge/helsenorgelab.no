# Generated by Django 2.0.9 on 2019-01-18 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standardpages', '0004_auto_20190108_1308'),
        ('images', '0004_auto_20190107_1643'),
        ('wagtailcore', '0040_page_draft_title'),
        ('home', '0003_remove_homepage_call_to_action'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='strapline',
            new_name='introduction',
        ),
        migrations.AddField(
            model_name='homepage',
            name='button_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='button_text',
            field=models.CharField(blank=True, max_length=55),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_page_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='standardpages.InformationPage'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_page_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='standardpages.InformationPage'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_page_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='standardpages.InformationPage'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_page_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='standardpages.InformationPage'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_page_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='standardpages.InformationPage'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_page_6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='standardpages.InformationPage'),
        ),
    ]
