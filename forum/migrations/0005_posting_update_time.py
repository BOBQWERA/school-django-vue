# Generated by Django 3.1.3 on 2020-11-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_posting_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]