# Generated by Django 3.1.5 on 2021-11-11 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='articles/authors/pictures/'),
        ),
    ]