from enum import unique

from django.db import models


@unique
class FormStateChoice(models.IntegerChoices):
    CREATED = 1, "Created"
    DELETED = 2, "Deleted"
    PUBLISHED = 3, "Published"


TEXT = "Text"
NUMBER = "Number"
EMAIL = "Email"
MULTIPLE_CHOICE = "MultipleChoice"

QUESTION_TYPE_LIST = [TEXT, NUMBER, EMAIL, MULTIPLE_CHOICE]

QUESTION_TYPES = (
    ("Text", TEXT),
    ("Number", NUMBER),
    ("Email", EMAIL),
    ("MultipleChoice", MULTIPLE_CHOICE),
    # Add more types here
)
