# Generated by Django 3.2 on 2023-05-31 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230531_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', to='reviews.Genre'),
        ),
    ]