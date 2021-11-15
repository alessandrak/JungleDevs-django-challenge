# Generated by Django 3.1.5 on 2021-11-13 18:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0002_auto_20211111_0018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('category', models.CharField(max_length=80)),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField()),
                ('first_paragraph', models.TextField()),
                ('body', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='authors.author')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]