# Generated by Django 3.1.4 on 2020-12-05 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20201128_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='append_file',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
