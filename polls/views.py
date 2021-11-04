# from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from polls.serializers import TeaSerializer
from .models import Users, Teas
from rest_framework.response import Response
from rest_framework.views import APIView
from smtplib import SMTP_SSL

# Create your views here.

def put():
    try:
        toEmail = 'cherry@make.education'
        fromEmail = 'connect@teave.co.kr'
        TitleEmail = '이메일 제목입니다'

        msg = "\r\n".join([
            "From: " + fromEmail,
            "To: " + toEmail,
            "Subject: " + TitleEmail,
            "",
            "여기에 내용이 들어갑니다"
        ])

        ## Daum SMTP
        conn = SMTP_SSL("smtp.daum.net:465")
        conn.ehlo()

        loginId = 'connect@teave.co.kr'
        loginPassword = 'ekdmadyd1!'
        conn.login(loginId, loginPassword)

        conn.sendmail(fromEmail, toEmail, msg)
        conn.close()
        return 'Success to send emails.'


    except Exception as e:
        return "Failed. error" + str(e)


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
