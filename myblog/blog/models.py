from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()\
                .filter(status=Post.Status.PUBLISHED)

# Create your models here.
class Post(models.Model):
    
    """
        Usamos la clase status como un enum
    """
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    
    # Trae todos los objetos
    objects = models.Manager()
    # Trae solo los publicados
    published = PublishedManager()
    
    """
        Es la metadata del modelo
    """
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
    
    """
        Transforma el registro en un string
        en caso de necesitarlo para una vista.
        En este caso, cuando llamemos un post como
        string, nos traera el titulo.
    """
    def __str__(self) -> str:
        return self.title