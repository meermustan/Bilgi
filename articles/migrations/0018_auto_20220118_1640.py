# Generated by Django 3.2 on 2022-01-18 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0017_rename_comments_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='Comment',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Replay_Comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Replay_Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replay_comment', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.comment')),
            ],
        ),
    ]
