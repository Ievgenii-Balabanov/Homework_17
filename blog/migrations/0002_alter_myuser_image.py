# Generated by Django 4.2.3 on 2023-08-09 21:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="image",
            field=models.ImageField(upload_to="images"),
        ),
    ]
