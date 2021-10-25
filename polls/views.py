# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from polls.serializers import TeaSerializer
from .models import Users, Teas
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


def index(request):
    print(request)
    return HttpResponse("hello, we are pirates")


def post_view(request):
    temps = Teas.objects.all()
    tt = []
    for temp in temps:
        print(temp.name, temp.id)
        tt.append(temp.name)
    print(temps)
    return HttpResponse(tt)
    # return HttpResponse(temps)


class TeaListAPI(APIView):
    def get(self, request):
        queryset = Teas.objects.all()
        print(queryset)
        serializer = TeaSerializer(queryset, many=True)
        return Response(serializer.data)
