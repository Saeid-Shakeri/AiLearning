from django.db import models
from course.models import Professor, Category
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User

# Create your models here.

class Article(models.Model):
    name = models.CharField(max_length=150,help_text='The titile of Article')
    body = models.TextField( null=True, blank=True)
    author = models.ManyToManyField(to=Professor)
    date = models.DateField()
    file = models.FileField(null=True,blank=True,upload_to='media/article/file/')
    image = models.ImageField(null=True,blank=True,upload_to='media/article/image/')
    category = models.ForeignKey(to=Category,on_delete=models.PROTECT,null=True)
    slug = models.SlugField(unique=True)
    video = models.FileField(null=True,blank=True,upload_to='media/article/video/')
    rates = models.PositiveIntegerField(default=0)
    readers = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )

    def save(self, *args, **kwargs):
        self.score = round(self.score, 1)
        super(Article, self).save(*args, **kwargs)


    class Meta:
        verbose_name =("Article")
        verbose_name_plural = ("Articles")

    def __str__(self):
        return f'{self.name}'
    

class ArticleRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.PROTECT)
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE)


class ArticleComment(models.Model):
    content = models.CharField(max_length=250, null=True, help_text="Comment text")
    email = models.EmailField()
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    article = models.ForeignKey(to=Article,on_delete=models.PROTECT, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )

    class Meta:
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'

    def __str__(self):
        return f"Comment: {self.content}"