# Generated by Django 4.1.7 on 2023-04-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images/'),
        ),
    ]
