from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Blog
import json
import jwt
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY


@csrf_exempt
def create_blog(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_email = request.user_payload.get('email') 
        blog = Blog(
            createdBy=user_email,
            title=data.get('title', ''),
            description=data.get('description', ''),
            content=data.get('content', '')
        )
        blog.save()
        return JsonResponse({
            'status': 201,
            'message': 'Blog created successfully',
            'id': str(blog.id),
            'createdBy': blog.createdBy,
            'title': blog.title,
            'description': blog.description,
            'content': blog.content,
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)