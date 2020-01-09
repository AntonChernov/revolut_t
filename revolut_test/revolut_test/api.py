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
    """
    API for Nested
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request
        :param request: Request object
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return: JSON response
        :rtype:
        """
        # Try here not gud idea but for some reason
        # DRF(Django rest framework) return empty OrderedDict after validation
        # I believe problem related to newest version of Django(3.0.2)
        # DRF just not handle all changes
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
    """
    Create Token object for user when user save()
    :param sender:
    :type sender:
    :param instance:
    :type instance:
    :param created:
    :type created:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    if created:
        Token.objects.create(user=instance)