import jwt
from django.http import JsonResponse
from django.conf import settings
from django.urls import resolve

SECRET_KEY = settings.SECRET_KEY

# Define public endpoints that don't require authentication
PUBLIC_ENDPOINTS = [
    'register_user',
    'login_user',
    'get_blogs',  # If you want blogs to be publicly readable
]

def _extract_token(auth_header: str):
    if not auth_header:
        return None
    parts = auth_header.strip().split()
    if len(parts) >= 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Initialize JWT attributes
        request.jwt_payload = None
        request.jwt_user_id = None
        
        # Skip authentication for public endpoints
        try:
            url_name = resolve(request.path_info).url_name
            if url_name in PUBLIC_ENDPOINTS:
                return self.get_response(request)
        except:
            pass
        
        # Skip authentication for admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)

        token = _extract_token(request.headers.get("Authorization"))
        if not token:
            return JsonResponse({'error': 'Authorization header missing or invalid format'}, status=401)

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.jwt_payload = decoded
            request.jwt_user_id = decoded.get("user_id")
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return self.get_response(request)
