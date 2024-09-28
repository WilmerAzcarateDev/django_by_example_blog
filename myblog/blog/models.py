from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    
    """Transforma el registro
    """
    def __str__(self) -> str:
        return super().__str__()