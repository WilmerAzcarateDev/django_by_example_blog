from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

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
    slug = models.SlugField(max_length=250,unique_for_date='publish')
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
    # Manipula las etiquetas
    tags = TaggableManager()
    
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
    
    """
        Crea una url unica para cada registro
        en la tabla de blogs
    """
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug])
        
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
    
    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'