# Generated by Django 4.1.9 on 2023-07-07 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("status", models.CharField(max_length=100)),
                ("folder_name", models.CharField(default="", max_length=100)),
                ("cid_metadata", models.TextField(default="", max_length=255)),
                ("cid_nfts", models.TextField(default="", max_length=255)),
            ],
        ),
    ]
