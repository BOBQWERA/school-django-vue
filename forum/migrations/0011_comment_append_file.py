# Generated by Django 3.1.4 on 2020-12-05 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_auto_20201130_2036'),
        ('forum', '0010_remove_comment_append_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='append_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.files'),
        ),
    ]
