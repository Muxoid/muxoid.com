# Generated by Django 5.1.6 on 2025-03-01 04:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0004_blogpost_directory_note_directory"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
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
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("pub_date", models.DateTimeField(verbose_name="date published")),
                (
                    "directory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portfolio.directory",
                    ),
                ),
            ],
        ),
    ]
