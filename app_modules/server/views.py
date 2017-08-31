# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess
import json
import requests

from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response


RABBIT_API = getattr(settings, 'RABBITMQ_DEFAULT_WEB_API')
RABBIT_USERNAME = getattr(settings, 'RABBITMQ_DEFAULT_USER')
RABBIT_PASSWORD = getattr(settings, 'RABBITMQ_DEFAULT_PASS')


modulesSubPath = '/server/script/linux_json_api.sh'
appRootPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class ServerHealthCheck(APIView):
    def get(self, request, *args, **kwargs):
        if 'module' in request.GET:
            module = self.request.GET['module']
            output = subprocess.Popen(
                appRootPath + modulesSubPath + " " + module,
                shell=True,
                stdout=subprocess.PIPE)
            data = output.communicate()[0]
            test = data.replace("\\", '')
            report = test.replace("\\", '')
            reports = json.loads(report)
            return Response(reports)
        else:
            Response({}, status=200)



class RabbitMQServerHealthChaeck(APIView):
    """
    THIS API GETS YOU ALL THE HEALTH OPTIONS FOR RABBITMQ
    see http://127.0.0.1:15672/api/ for more options
    """

    def get(self, request, *args, **kwargs):
        try:
            s = requests.Session()
            s.auth = (RABBIT_USERNAME, RABBIT_PASSWORD)
            if 'method' in request.GET and not 'sort' in request.GET:
                rabbit_api = s.get(RABBIT_API + request.GET['method'])
            elif 'method' in request.GET and 'sort' in request.GET:
                rabbit_api = s.get(RABBIT_API + request.GET['method'], params=request.GET['sort'])
            else:
                return Response('Please Specify A method For the API', status=404)
            data = json.loads(rabbit_api.content)
            return Response(data, status=200)
        except Exception as e:
            print e
            return Response({}, status=500)

