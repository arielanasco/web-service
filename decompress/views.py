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
import codecs

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
            raise Exception("URL should not be empty.") 

        with requests.get(url, stream=True) as data:
            if data.status_code != 200:
                raise Exception("File not found on the server") 

            # data_headers = data.headers.get('content-disposition').decode('UTF-8')
            # print(data_headers)
            # filename = re.findall('filename=(.+)', data_headers)[0]
            # is_valid_file = filename.endswith('gz',-3,-1)

            with gzip.open(path, "wb") as output:
                for chunk in data.iter_content(chunk_size=16*1024):
                    output.write(chunk)
                # with io.TextIOWrapper(output, encoding='utf-8') as encode:
                #     for chunk in data.iter_content(chunk_size=16*1024):
                #         encode.write(codecs.decode(chunk, 'utf-8'))

        # if not is_valid_file:
            # os.remove("temp.log.gz")
            # raise Exception("File should be gzip only")

        with gzip.open(path, 'rb') as ip:
                with io.TextIOWrapper(ip, encoding='utf-8') as decoder:
                    content = decoder.read()

        return HttpResponse(f"{content}",content_type="text/plain", status=status.HTTP_200_OK)

    else:
        return Response({"error":f'Invalid Key Provided'},status=status.HTTP_400_BAD_REQUEST)

def test_form(request):
    return render (request, "decompress/test-form.html")

