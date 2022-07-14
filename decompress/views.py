from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
import gzip
import os
import io
from django.conf import settings
import re
from gzip import BadGzipFile
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}


@api_view(('POST',))
def index(request):
    url = request.POST.get('url', None)
    client_key = request.POST.get('client-key', None)
    print(url)
    print(client_key)
    path = r"/var/www/dev-webservice/temp.log.gz"
    if client_key in settings.CLIENT_KEY:
        if not url:
            return Response({"error":f'URL should not be empty.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            with requests.get(url, stream=True) as data:
                if data.status_code != 200:
                    return Response({"error":f'File not found on the server.'},status=status.HTTP_400_BAD_REQUEST)
                open(path, 'wb').write(data.content)
        except Exception as err:
            return Response({"error":f'{err}'},status=status.HTTP_400_BAD_REQUEST)
            
        try:
            with gzip.open(path, 'rb') as ip:
                    with io.TextIOWrapper(ip, encoding='utf-8') as decoder:
                        content = decoder.read()

            return HttpResponse(f"{content}",content_type="text/plain", status=status.HTTP_200_OK)
        except BadGzipFile:
            return Response({"error":f'Not a gzip file.'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error":f'Invalid Key Provided'},status=status.HTTP_400_BAD_REQUEST)

def test_form(request):
    return render (request, "decompress/test-form.html")

