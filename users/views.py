import json, re, bcrypt, jwt, random

from django.http.response import JsonResponse
from django.views         import View

from users.models         import Member
from my_settings          import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            id       = re.compile("[a-z0-9]{5,19}$")
            password = re.compile("[0-9]{8,16}")
            email    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-z0-9-]+\.[a-zA-z0-9-]+$")
            
            if  not password.match(data['password']) or not id.match(data['account']) or not email.match(data['email']):
                return JsonResponse({'message':' INVALID_FORMAT'}, status=400)
            
            if Member.objects.filter(account = data["account"]).exists():
                return JsonResponse({"message": "ALREADY_EXIST"}, status=400)

            encoded_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            Member.objects.create(
                account      = data['account'],
                password     = encoded_pw.decode('utf-8'),
                name         = data['name'],
                address      = data['address'],
                phone_number = data['phone_number'],
                email        = data['email'],
                points       = random.randrange(10000, 1000000)
             )
            return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)


class SignInView(View):
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
