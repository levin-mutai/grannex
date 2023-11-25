# Generated by Django 4.2.7 on 2023-11-24 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Categories",
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
                ("category", models.CharField(max_length=200)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Jobs",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("company", models.CharField(max_length=200)),
                ("location", models.CharField(max_length=200)),
                ("url", models.URLField()),
                ("application_deadline", models.DateField()),
                ("description", models.TextField()),
                ("title", models.CharField(max_length=200)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="jobs.categories",
                    ),
                ),
            ],
            options={
                "verbose_name": "Job",
                "verbose_name_plural": "Jobs",
                "ordering": ["created_at"],
                "get_latest_by": "created_at",
            },
        ),
        migrations.CreateModel(
            name="Applicants",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("phone", models.CharField(max_length=200)),
                ("resume", models.FileField(upload_to="resumes")),
                ("cover_letter", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "pending"),
                            ("accepted", "accepted"),
                            ("rejected", "rejected"),
                            ("withdrawn", "withdrawn"),
                        ],
                        default="pending",
                        max_length=200,
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.jobs"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Applicant",
                "verbose_name_plural": "Applicants",
                "ordering": ["created_at"],
                "get_latest_by": "created_at",
            },
        ),
        migrations.AddIndex(
            model_name="jobs",
            index=models.Index(
                fields=["-created_at"], name="jobs_jobs_created_3055a3_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="applicants",
            index=models.Index(
                fields=["-created_at"], name="jobs_applic_created_21d9ff_idx"
            ),
        ),
    ]