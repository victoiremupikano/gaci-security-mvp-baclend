# Generated by Django 4.0 on 2023-06-27 10:01

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_assignment_agent_remove_assignment_function_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=authentication.models.get_image_path),
        ),
    ]
