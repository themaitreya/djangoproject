from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def user_profile_image_path(instance, filename):
    return f'profile_images/{instance.username}/{filename}'

#프로필 이미지, 팔로우 팔로잉 수
class User(AbstractUser):
    profile_image = models.ImageField(upload_to = user_profile_image_path, blank = True, null = True)
    
    #팔로우
    follows = models.ManyToManyField('self', symmetrical = False, related_name = 'followers', blank = True)
    
    @property
    def follwer_count(self):
        return self.followers.count()
    
    @property
    def follwing_count(self):
        return self.follows.count()
    
    def __str__(self):
        return self.username
    