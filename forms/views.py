from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

import common.error_codes as ec
import common.success_codes as sc
from common.utils import submit_exception_on_sentry
from forms.utils import (
    create_question_util,
    get_form_questions_util,
    publish_form_util,
    submit_answers_util,
)

from .models import Form
from .serializers import FormCreateSerializer, FormResponseSerializer


class FormGetView(RetrieveAPIView):
    response_serializer_class = FormResponseSerializer

    def get_queryset(self):
        return Form.objects.filter(uid=self.uid)

    def get(self, request, *args, **kwargs):
        try:
            self.uid = kwargs.get("form_uid")
            data = self.response_serializer_class(self.get_queryset(), many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            return Response(data=ec.FORM_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            submit_exception_on_sentry(e)
            return Response(
                data=ec.UNEXPECTED_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FormCreateView(CreateAPIView):
    serializer_class = FormCreateSerializer
    response_serializer_class = FormResponseSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def get_author(self):
        return User.objects.get(id=1)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            form = self.perform_create(serializer)
            response_serializer = self.response_serializer_class(instance=form)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            submit_exception_on_sentry(e)
            return Response(
                data=ec.UNEXPECTED_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class QuestionsView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            form_uid = kwargs.get("form_uid")
            response = get_form_questions_util(form_uid)
            return Response(data=response, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            return Response(data=ec.FORM_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            submit_exception_on_sentry(e)
            return Response(
                data=ec.UNEXPECTED_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, *args, **kwargs):
        try:
            form_uid = kwargs.get("form_uid")
            create_question_util(form_uid, request)
            return Response(data=sc.GENERIC_SUCCESS, status=status.HTTP_201_CREATED)
        except Form.DoesNotExist:
            return Response(data=ec.FORM_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            submit_exception_on_sentry(e)
            return Response(
                data=ec.UNEXPECTED_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AnswersView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            form_uid = kwargs.get("form_uid")
            submit_answers_util(form_uid, request)
            return Response(data=sc.GENERIC_SUCCESS, status=status.HTTP_201_CREATED)
        except Form.DoesNotExist:
            return Response(data=ec.FORM_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            submit_exception_on_sentry(e)
            return Response(
                data=ec.UNEXPECTED_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FormPublishView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            form_uid = kwargs.get("form_uid")
            response = publish_form_util(form_uid)
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Form.DoesNotExist:
            return Response(data=ec.FORM_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            submit_exception_on_sentry(e)
            return Response(
                data=ec.UNEXPECTED_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
