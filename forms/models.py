import uuid

from django.db import models

from fms.settings import FMS_BASE_URL
from forms.constants import QUESTION_TYPES, FormStateChoice


def generate_uid():
    return str(uuid.uuid4())


class Form(models.Model):
    uid = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    state = models.IntegerField(choices=FormStateChoice.choices, default=FormStateChoice.CREATED)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    commands = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.uid}"

    @property
    def is_published(self):
        return self.state == FormStateChoice.PUBLISHED

    @property
    def link(self):
        # Logic for creating link to the form
        # For simplicity I am returning this as of now
        return f"{FMS_BASE_URL}/forms/{self.uid}"


class Question(models.Model):
    uid = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    rank = models.IntegerField()
    type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # generate UID for new response object
            self.uid = generate_uid()
        super().save(*args, **kwargs)


class Option(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")


class QuestionResponse(models.Model):
    uid = models.CharField(max_length=50, unique=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")
    respondent_name = models.CharField(max_length=255)
    respondent_email = models.EmailField()
    respondent_phone = models.CharField(max_length=255)
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid()
        super().save(*args, **kwargs)


class Answer(models.Model):
    response = models.ForeignKey(QuestionResponse, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField()
