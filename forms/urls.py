from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("", views.FormCreateView.as_view(), name="form-create-view"),
    path("<form_uid>/", views.FormGetView.as_view(), name="form-get-view"),
    path(
        "<form_uid>/publish/",
        views.FormPublishView.as_view(),
        name="form-publish-view",
    ),
    path(
        "<form_uid>/questions/",
        views.QuestionsView.as_view(),
        name="questions-view",
    ),
    path(
        "<form_uid>/questions/submit-answers/",
        views.AnswersView.as_view(),
        name="submit-answers-view",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
