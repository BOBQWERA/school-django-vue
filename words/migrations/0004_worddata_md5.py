# Generated by Django 3.1.4 on 2020-12-15 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0003_wordplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='worddata',
            name='md5',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
