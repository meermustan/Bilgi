# Generated by Django 3.2 on 2022-01-22 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_comment_replay_comment_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='replay_comment_text',
        ),
    ]
