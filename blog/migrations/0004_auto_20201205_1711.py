# Generated by Django 3.1.4 on 2020-12-05 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examine', '0001_initial'),
        ('blog', '0003_blog_ex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='ex',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='examine.examine'),
            preserve_default=False,
        ),
    ]
