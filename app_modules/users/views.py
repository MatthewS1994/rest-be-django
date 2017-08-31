# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import permissions, viewsets
from .permissions import IsAccountOwner
from .serializers import AccountSerializer
from .models import Account
from rest_framework import status
from rest_framework.response import Response


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),IsAccountOwner())

        if self.request.method == 'POST':
            return (permissions.IsAuthenticated(),IsAccountOwner())
        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'})