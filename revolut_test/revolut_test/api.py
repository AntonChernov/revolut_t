# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from nest import DataHandler
from revolut_test.serializers import NestedListSerializer, NestedDataSerializer


class NestedView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        print(type(request.data))
        data_process = DataHandler(
            file_path=request.data,
            currency=self.request.query_params.get('currency')
        )

        result = data_process.result_builder(
            json_format=True
        )
        return Response(json.dumps(result))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)