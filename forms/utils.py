from django.db import transaction

from common.form_actions.google_sheets import google_sheets_client
from forms.constants import MULTIPLE_CHOICE, QUESTION_TYPE_LIST, TEXT, FormStateChoice
from forms.models import Answer, Form, Option, Question, QuestionResponse
from forms.serializers import QuestionBaseSerializer


def validate_question_type(question_type):
    if question_type not in QUESTION_TYPE_LIST:
        raise ValueError(f"Invalid question type: {question_type}")
    return question_type


def validate_options(options, question_type):
    if question_type == MULTIPLE_CHOICE:
        if len(options) < 2:
            raise ValueError("At least two options are required")

    return options


def validate_respondant_details(respondent_name, respondent_email, respondent_phone):
    if not respondent_name:
        raise ValueError("Respondent name is required")
    if not respondent_email:
        raise ValueError("Respondent email is required")
    if not respondent_phone:
        raise ValueError("Respondent phone is required")


def add_answer_row_util(form, question_answer_map, respondent_name, respondent_email, respondent_phone):
    total_response = QuestionResponse.objects.filter(form=form).count()
    sheet_id = form.metadata.get("sheet_id")
    questions = form.questions.all().order_by("rank")
    question_uids = [question.uid for question in questions]
    answer_list = []
    for question_uid in question_uids:
        if question_uid in question_answer_map.keys():
            answer_list.append(question_answer_map[question_uid])
        else:
            answer_list.append("")
    row_list = [respondent_name, respondent_email, respondent_phone]
    row_list.extend(answer_list)
    google_sheets_client.add_row(sheet_id, total_response + 1, row_list)


def get_form_questions_util(form_uid):
    form = Form.objects.get(uid=form_uid)
    return QuestionBaseSerializer(form.questions.all(), many=True).data


def create_question_util(form_uid, request):
    form = Form.objects.get(uid=form_uid)
    data = request.data
    question_title = data.get("title")
    question_description = data.get("description", "")
    question_type = data.get("type", TEXT)
    question_type = validate_question_type(question_type)
    options = data.get("options", [])
    options = validate_options(options, question_type)
    metadata = data.get("metadata", {})
    question_options = []
    for option in options:
        question_options.append(Option(text=option))

    with transaction.atomic():
        question = Question.objects.create(
            title=question_title,
            description=question_description,
            form=form,
            type=question_type,
            rank=form.questions.count() + 1,
            metadata=metadata,
        )

        for question_option in question_options:
            question_option.question = question

        if question_type == MULTIPLE_CHOICE:
            Option.objects.bulk_create(question_options)


def submit_answers_util(form_uid, request):
    form = Form.objects.get(uid=form_uid)
    if not form.is_published:
        raise ValueError("Form is not published")
    data = request.data
    respondent_name = data.get("respondent_name", None)
    respondent_email = data.get("respondent_email", None)
    respondent_phone = data.get("respondent_phone", None)
    validate_respondant_details(respondent_name, respondent_email, respondent_phone)
    metadata = data.get("metadata", {})
    answers = data.get("answers", [])
    if len(answers) == 0:
        raise ValueError("At least one answer is required")
    question_answer_map = {answer["question_uid"]: str(answer["value"]) for answer in answers}
    questions = Question.objects.filter(uid__in=list(question_answer_map.keys()), form=form)
    question_answers = [Answer(question=question, value=question_answer_map[question.uid]) for question in questions]
    if len(question_answers) == 0:
        raise ValueError("At least one answer is required")

    with transaction.atomic():
        response = QuestionResponse.objects.create(
            form=form,
            respondent_name=respondent_name,
            respondent_email=respondent_email,
            respondent_phone=respondent_phone,
            metadata=metadata,
        )

        for question_answer in question_answers:
            question_answer.response = response

        Answer.objects.bulk_create(question_answers)

    if "GOOGLE_SHEET" in form.commands.split(","):
        add_answer_row_util(form, question_answer_map, respondent_name, respondent_email, respondent_phone)


def publish_form_util(form_uid):
    form = Form.objects.get(uid=form_uid)
    if form.is_published:
        raise ValueError("Form is already published")

    if form.questions.count() == 0:
        raise ValueError("At least one question is required")

    form.state = FormStateChoice.PUBLISHED
    if "GOOGLE_SHEET" in form.commands.split(","):
        sheet_id = google_sheets_client.create_sheet(form.title)
        questions = form.questions.all().order_by("rank")
        question_titles = [question.title for question in questions]
        row_list = ["respondent_name", "respondent_email", "respondent_phone"]
        row_list.extend(question_titles)
        google_sheets_client.add_row(sheet_id, 1, row_list)
        form.metadata["sheet_id"] = sheet_id

    form.save()
    return {"link": form.link}
