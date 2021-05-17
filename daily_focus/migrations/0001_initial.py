# Generated by Django 3.2 on 2021-05-13 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Focus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.CharField(max_length=300)),
                ('station', models.CharField(max_length=300)),
                ('focus_content', models.TextField(blank=True)),
                ('focus_start', models.DateField()),
                ('focus_end', models.DateField()),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='focus', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FocusImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d')),
                ('focus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to='daily_focus.focus')),
            ],
        ),
    ]