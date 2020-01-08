# -*- coding: utf-8 -*-
from rest_framework import serializers


class NestedDataSerializer(serializers.Serializer):

    country = serializers.CharField(allow_null=False, required=True),
    city = serializers.CharField(allow_null=False, required=True),
    currency = serializers.CharField(allow_null=False, required=True),
    amount = serializers.FloatField(allow_null=False, required=True),

    def validate_amount(self, value):
        """
        Validate amount field
        """
        if isinstance(value['amount'], int):
            return float(value['amount'])
        return value['amount']


class NestedListSerializer(serializers.Serializer):

    data_list = NestedDataSerializer(many=True)
