from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

def check_jwt(request):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed("No JWT token provided.")

    token_str = auth_header.split(' ')[1]
    try:
        token = AccessToken(token_str)  # 토큰 유효성 검증
        user_id = token['user_id']  # JWT에 포함된 사용자 ID
        return user_id
    except Exception as e:
        raise AuthenticationFailed(f"Invalid JWT token: {str(e)}")
