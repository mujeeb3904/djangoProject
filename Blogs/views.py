from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Blog
from User.models import User
import json


@csrf_exempt
def create_blog(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    user_id = getattr(request, 'jwt_user_id', None)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized: missing or invalid token'}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found for provided token'}, status=404)

    blog = Blog.objects.create(
        createdBy=user,
        title=data.get('title', ''),
        description=data.get('description', ''),
        content=data.get('content', '')
    )

    return JsonResponse({
        'status': 201,
        'message': 'Blog created successfully',
        'id': str(blog.id),
        'createdById': str(user.id),
        'title': blog.title,
        'description': blog.description,
        'content': blog.content,
    }, status=201)

@csrf_exempt
def get_blogs(request): 
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    blogs = Blog.objects.all()
    return JsonResponse({
        'status': 200,
        'message': 'Blogs fetched successfully',
        'blogs': [{
            'id': str(blog.id),
            'createdById': str(blog.createdBy.id),
            'title': blog.title,
            'description': blog.description,
            'content': blog.content,
        } for blog in blogs]
    }, status=200)

