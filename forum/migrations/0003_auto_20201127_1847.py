# Generated by Django 3.1.3 on 2020-11-27 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20201127_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='urlname',
            field=models.CharField(max_length=20),
        ),
    ]