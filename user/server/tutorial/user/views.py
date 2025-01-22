from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserDetailView(APIView):
    #permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        """
        GET 요청: 현재 로그인된 유저 정보를 반환
        """
        user = request.user  # 현재 로그인된 사용자
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        PUT 요청: 현재 로그인된 유저 정보를 수정
        """
        user = request.user  # 현재 로그인된 사용자
        serializer = UserSerializer(user, data=request.data, partial=True)  # 부분 업데이트 허용
        if serializer.is_valid():
            serializer.save()  # 유저 정보 저장
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
