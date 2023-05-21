from django import forms

from .models import Question


class TextQuestionForm(forms.Form):
    def __init__(self, question_id, *args, **kwargs):
        self.question_id = question_id
        super().__init__(*args, **kwargs)

    answer = forms.CharField(max_length=100)

    def clean_answer(self):
        answer = self.cleaned_data["answer"]
        question = Question.objects.get(id=self.question_id)
        if len(answer) > question.max_length:
            raise forms.ValidationError(f"Answer must be less than or equal to {question.max_length} characters")
        return answer
