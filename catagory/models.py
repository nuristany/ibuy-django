from django.db import models
from django.urls import reverse

# Create your models here.
class Catagory(models.Model):
    catagory_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to= 'photo/catagories', blank=True)
    
    class Meta:
        verbose_name = 'catagory'
        verbose_name_plural = 'catagories'    
    
    def get_url(self):
        return reverse('products_by_catagory', args=[self.slug])
    
    def __str__(self):
        return self.catagory_name
        
        