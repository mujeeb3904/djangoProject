import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from bson.objectid import ObjectId
from .models import User
import bcrypt
import jwt
import datetime
from django.conf import settings

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Check if email already exists
        if User.objects(email=data['email']).first():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # Hash password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Create user
        user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password.decode('utf-8')
        )
        user.save()

        return JsonResponse({
            'status': 'success',
            'message': 'User registered successfully',
            'data': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        # Find user
        user = User.objects(email=data['email']).first()
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        # Verify password
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user.id),
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Reduced from 10 days
        }, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': {
                    'id': str(user.id),
                    'name': user.name,
                    'email': user.email,
                },
                'token': token
            }
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

# Protected endpoint - requires authentication
@require_http_methods(["GET"])
def get_user_profile(request):
    user_id = request.jwt_user_id
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request):
    user_id = request.jwt_user_id
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)
        
        # Update fields if provided
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if new email already exists
            existing_user = User.objects(email=data['email']).first()
            if existing_user and str(existing_user.id) != user_id:
                return JsonResponse({'error': 'Email already exists'}, status=400)
            user.email = data['email']
        
        user.updated_at = datetime.datetime.utcnow()
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'User updated successfully',
            'data': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
