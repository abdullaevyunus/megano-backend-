# Generated by Django 3.2.24 on 2024-04-08 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='full_description',
            new_name='fullDescription',
        ),
    ]
