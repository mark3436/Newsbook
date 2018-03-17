from django.http import HttpResponse
from .models import Newss, Publishers
import json
from rest_framework import permissions
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateUserSerializer, NewsSerializer



class NewsList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        all_news = Newss.objects.all()[:10]
        listdata = []
        for i in range(len(all_news)):
            all_news[i].image_url = all_news[i].image_url.split(' ')
        #serializer = NewsSerializer(all_news, many=True)
        for news in all_news:
            listdata.append({'id': news.id,'publisher_id': news.publisher_id, 'topic': news.topic, 'title' : news.title, 'body': news.body, 'datetime': str(news.datetime), 'image_url': news.image_url})
        jsondata = {'result' : listdata}
        return Response(jsondata)
        #return HttpResponse(json.dumps(jsondata, ensure_ascii=False).encode('utf8'), content_type="application/json")

class CreateUser(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            #return HttpResponse('<h1> {{ serializer.username }} </h1>')
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
def add(request):
    df = pd.read_csv('C:/Users/Mark/Downloads/Documents/Project/newsbook/topicmodeling/todb.csv',low_memory=False)
    publisher1 = Publisher.objects.get(pk=1)
    for i in range(len(df)):
        news = Newss(publisher = publisher1, title = str(df['title'][i]), topic = str(df['topic'][i]), image_url = str(df['image_url'][i]), reference_id = str(df['reference_id'][i]), datetime = str(df['datetime'][i]), body = str(df['body'][i]))
        news.save()
