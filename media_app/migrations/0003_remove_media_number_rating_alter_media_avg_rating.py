# Generated by Django 5.1 on 2024-09-13 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_app', '0002_alter_review_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='number_rating',
        ),
        migrations.AlterField(
            model_name='media',
            name='avg_rating',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]