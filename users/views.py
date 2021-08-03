from users.models import *
from django.http.response import JsonResponse
from django.views import View
from jwt import algorithms
from .models import *
import re, bcrypt, jwt, json
from my_settings import SECRET_KEY
import string
import secrets
import random

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Id        = re.compile("[a-z0-9]{5,19}$")
            Password  = re.compile("[0-9]{8,16}")
            Email     = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-z0-9-]+\.[a-zA-z0-9-]+$")
            
            if  Password.match(data['password'])  is None or Id.match(data['account']) is None or Email.match(data['email']) is None:
                return JsonResponse({'message':' INVALID_FORMAT'}, status=400)
            
            if Member.objects.filter(account = data["account"]).exists():
                return JsonResponse({"message": "Already_Exist"}, status=400)

            encoded_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            point = random.randrange(10000, 1000000)

            Member.objects.create(
                account      = data['account'],
                password     = encoded_pw.decode('utf-8'),
                name         = data['name'],
                address      = data['address'],
                phone_number = data['phone_number'],
                email        = data['email'],
                points       = point
             )

            return JsonResponse({'message': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)



class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not Member.objects.filter(account=data['account']).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            member = Member.objects.get(account=data['account'])
            
            if not bcrypt.checkpw(data['password'].encode('utf-8'), member.password.encode('utf-8')):
                return JsonResponse({"message": "UNAUTHORIZED"}, status=401)
                
            token = jwt.encode({'id': member.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({"TOKKEN": token}, status=200)              
                
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)





class FindmemberView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not Member.objects.filter(email = data['email'], name=data['name']).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            member = Member.objects.get(email = data['email'], name=data['name'])

            result = []
            result.append({
                "name"    : member.name,
                "account" : member.account,
                "email"   : member.email  
            })

            return JsonResponse({"RESULT" : result}, status = 200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


    def patch(self, request):
        try:
            data = json.loads(request.body)
            if not Member.objects.filter(account=data['account'], name=data['name'], email=data['email']).exists():
                return JsonResponse({"message": "NOT_EXIST_POST"}, status=400)
            
            member        = Member.objects.get(account=data['account'], name=data['name'], email=data['email'])
            string_pool   = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(string_pool) for i in range(10))
            encoded_pw    = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt())

            member.password = encoded_pw.decode('utf-8')

            member.save()

            return JsonResponse({"MESSAGE": temp_password}, status=200)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)