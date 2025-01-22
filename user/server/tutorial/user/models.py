from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        db_table = "custom_user"


class Friends(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    friends = models.ManyToManyField('self', blank=True, symmetrical=True) # symmetrical -> 상대 유저도 친구관계로 등록됨

    class Meta:
        db_table = "friends"
        
    def __str__(self):
        return self.user.username

    def add_friend(self, friend):
        """친구 추가 메서드"""
        if friend != self:  # 자기 자신을 친구로 추가하지 않도록 방지
            self.friends.add(friend)

    def remove_friend(self, friend):
        """친구 삭제 메서드"""
        self.friends.remove(friend)

    def get_friends(self):
        """현재 친구 목록 반환"""
        return self.friends.all()


class Dashboard(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    stats = models.JSONField(default=dict)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dashboard"
