# Generated by Django 3.1.5 on 2021-11-15 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_auto_20211111_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='authors/pictures/'),
        ),
    ]
