from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import re

# 상품 이미지 저장하는 경로
def product_image_path(instance, filename):
    return f'product_images/{instance.user.username}/{filename}'

#공백과 특수문자를 불허하는 함수
def validation_hashtag(value):
    if not re.match(r'[0-9a-zA-Z_]+$', value):
        raise ValidationError('해시태그는 언어, 숫자만 가능함!')
    
#해시태그를 선언하고 저장함
class HashTag(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validation_hashtag])

    def __str__(self):
        return f'#{self.name}'
    
#사용자가 등록한 상품을 저장함
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name= 'products')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to = product_image_path, blank =True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    #상품 좋아요 설정. 다대다설정!
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liked_products', blank=True)
    
    #상품과 연결되는 해시태그
    hashtags = models.ManyToManyField(HashTag, related_name='products',blank=True)
    
    #상품조회수
    views = models.PositiveIntegerField(default=0)
    
    def like_count(self):
        return self.likes.count()
    def __str__(self):
        return self.title