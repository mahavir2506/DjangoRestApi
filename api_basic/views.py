from django.contrib.admin.options import csrf_protect_m
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, response
from rest_framework.parsers import JSONParser
from .serializers import ArticleSerializers
from .models import Article
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.
class ArticleList(APIView):
    def get(self,request):
        article=Article.objects.all()
        serialzer=ArticleSerializers(article,many=True)
        return Response(serialzer.data)
    
    def post(self,request):
        serialzer=ArticleSerializers(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ArticleDetail(APIView):
    def get_object(self,id):
        try:
            #return HttpResponse("<h1> Hello World</h1>")
            a=Article.objects.get(id=id)
            return a
        except Article.DoesNotExist:
            return None
    def get(self,request,id):
       a=self.get_object(id)
       if a is None:
           return Response(status=status.HTTP_204_NO_CONTENT)
       serializer = ArticleSerializers(a)
       return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self,request,id):
        serializer = ArticleSerializers(self.get_object(id),data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request,id):
        self.get_object(id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

