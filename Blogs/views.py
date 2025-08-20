from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Blog
from User.models import User
import json
import datetime

@csrf_exempt
@require_http_methods(["POST"])
def create_blog(request):
    user_id = request.jwt_user_id
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['title', 'description', 'content']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Get user
        user = User.objects.get(id=user_id)
        
        # Create blog
        blog = Blog(
            createdBy=user,
            title=data['title'],
            description=data['description'],
            content=data['content']
        )
        blog.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Blog created successfully',
            'data': {
                'id': str(blog.id),
                'title': blog.title,
                'description': blog.description,
                'content': blog.content,
                'created_by': {
                    'id': str(user.id),
                    'name': user.name
                },
                'created_at': blog.created_at.isoformat()
            }
        }, status=201)
        
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

@require_http_methods(["GET"])
def get_blogs(request):
    try:
        blogs = Blog.objects.all()
        blogs_data = []
        
        for blog in blogs:
            blogs_data.append({
                'id': str(blog.id),
                'title': blog.title,
                'description': blog.description,
                'content': blog.content,
                'created_by': {
                    'id': str(blog.createdBy.id),
                    'name': blog.createdBy.name
                },
                'created_at': blog.created_at.isoformat(),
                'updated_at': blog.updated_at.isoformat()
            })
        
        return JsonResponse({
            'status': 'success',
            'message': 'Blogs fetched successfully',
            'data': blogs_data
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

@require_http_methods(["GET"])
def get_user_blogs(request):
    user_id = request.jwt_user_id
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        user = User.objects.get(id=user_id)
        blogs = Blog.objects(createdBy=user)
        
        blogs_data = [{
            'id': str(blog.id),
            'title': blog.title,
            'description': blog.description,
            'content': blog.content,
            'created_at': blog.created_at.isoformat(),
            'updated_at': blog.updated_at.isoformat()
        } for blog in blogs]
        
        return JsonResponse({
            'status': 'success',
            'data': blogs_data
        })
        
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

