# Generated by Django 4.2.3 on 2023-08-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0005_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]