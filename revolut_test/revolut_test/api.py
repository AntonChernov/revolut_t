# -*- coding: utf-8 -*-
import json
import logging

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

logger = logging.getLogger(__name__)

class NestedView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        try:
            data_process = DataHandler(
                file_path=request.data,
                currency=self.request.query_params.get('currency')
            )

            result = data_process.result_builder(
                json_format=True
            )
        except Exception as e:
            logger.debug('error is raised!: {0}'.format(e))
            return Response(status=400)
        else:
            return Response(json.dumps(result))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)