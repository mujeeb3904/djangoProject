import jwt
from django.http import JsonResponse
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY


def _extract_token(auth_header: str):
    if not auth_header:
        return None
    parts = auth_header.strip().split()
    if len(parts) == 1:
        return parts[0]  
    if len(parts) >= 2 and parts[0].lower() in ("bearer", "jwt"):
        return parts[1] 
    return parts[-1]      


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.jwt_payload = None
        request.jwt_user_id = None

        token = _extract_token(request.headers.get("Authorization"))
        if token:
            try:
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                request.jwt_payload = decoded
                request.jwt_user_id = decoded.get("user_id") or decoded.get("id")
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

        return self.get_response(request)
