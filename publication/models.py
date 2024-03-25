from django.db import models
from course.models import Professor, Category, Comment
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField( null=True, blank=True)
    author = models.ManyToManyField(to=Professor)
    date = models.DateField()
    file = models.FileField(null=True,blank=True,upload_to='static/article/file/')
    image = models.ImageField(null=True,blank=True,upload_to='static/article/image/')
    score = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(to=Category,default='Free',on_delete=models.SET_DEFAULT)
    comment = models.ForeignKey(to=Comment,on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name =("Article")
        verbose_name_plural = ("Articles")

    def __str__(self):
        return self.title