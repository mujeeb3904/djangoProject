import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from .models import User
import bcrypt
import jwt
import datetime
from django.conf import settings


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if User.objects(email=data['email']).first():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password.decode('utf-8')
        )
        user.save()

        return JsonResponse(
            {
                'status': 201,
                'message': 'User registered successfully',
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
            },
            status=201,
        )

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(email=data['email'])
            
       
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({
                    'user_id': str(user.id),
                    'email': user.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10)
                }, settings.SECRET_KEY, algorithm='HS256') 


                return JsonResponse({
                    'status': 200,
                    'message': 'User logged in successfully',
                    'id': str(user.id),
                    'name': user.name,
                    'email': user.email,
                    'token': token
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=user_id)
            user.name = data['name']
            user.email = data['email']
            user.updated_at = datetime.datetime.utcnow()
            user.save()
            return JsonResponse({'id': str(user.id), 'name': user.name, 'email': user.email})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=ObjectId(user_id))

            user.delete()
            return JsonResponse({'status': 200, 'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_user(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            return JsonResponse({'id': str(user.id), 'name': user.name, 'email': user.email})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_list = [{'id': str(u.id), 'name': u.name, 'email': u.email} for u in users]
        return JsonResponse(users_list, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
