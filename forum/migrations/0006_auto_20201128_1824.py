# Generated by Django 3.1.3 on 2020-11-28 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_posting_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='floor',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posting',
            name='floor',
            field=models.IntegerField(default=1),
        ),
    ]
