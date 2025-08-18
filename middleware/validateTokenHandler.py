import jwt
from django.http import JsonResponse
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1] 
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                request.user = decoded   
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = None  

        return self.get_response(request)
