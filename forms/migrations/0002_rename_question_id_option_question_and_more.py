# Generated by Django 4.2.1 on 2023-05-07 20:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="option",
            old_name="question_id",
            new_name="question",
        ),
        migrations.RemoveField(
            model_name="option",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="option",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="form",
            name="commands",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="type",
            field=models.CharField(
                choices=[
                    ("Text", "Text"),
                    ("Number", "Number"),
                    ("Email", "Email"),
                    ("MultipleChoice", "MultipleChoice"),
                ],
                max_length=50,
            ),
        ),
    ]
