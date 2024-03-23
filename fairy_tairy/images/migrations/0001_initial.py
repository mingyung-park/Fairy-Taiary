# Generated by Django 4.2.7 on 2024-02-15 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('diaries', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('image_url', models.URLField(null=True)),
                ('image_prompt', models.TextField(null=True)),
                ('diary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='diaries.diary')),
            ],
            options={
                'db_table': 'image',
                'managed': True,
            },
        ),
    ]
