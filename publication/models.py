from django.db import models
from django.utils import timezone
from course.models import Professor, Category
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User
import random
import string
from unidecode import unidecode
from django.utils.text import slugify



# Create your models here.


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a name character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(unidecode(instance.name))

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=5)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


class Article(models.Model):
    name = models.CharField(max_length=150,help_text='The titile of Article')
    body = models.TextField( null=True, blank=True)
    author = models.ManyToManyField(to=Professor)
    date = models.DateTimeField(default=timezone.now())
    file = models.FileField(null=True,blank=True,upload_to='media/article/file/')
    image = models.ImageField(null=True,blank=True,upload_to='media/article/image/')
    category = models.ForeignKey(to=Category,on_delete=models.PROTECT,null=True)
    slug = models.SlugField(unique=True, null=True,blank=True)
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
        if self.slug is None:
            self.slug = unique_slug_generator(self)
        super(Article, self).save(*args, **kwargs)


    class Meta:
        verbose_name =("Article")
        verbose_name_plural = ("Articles")

    def __str__(self):
        return f'{self.name}'
    

class ArticleRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True)
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE)


class ArticleComment(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField(help_text="Comment text")
    email = models.EmailField()
    # reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    checked = models.BooleanField(default=False)
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    # rates = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(to=User,related_name="article_likes",null=True,blank=True)
    dislikes = models.ManyToManyField(to=User,related_name="article_dislikes",null=True,blank=True)
    # score = models.FloatField(default=0,
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(5),
    #     ]
    # )

    class Meta:
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'

    def __str__(self):
        return f"{self.name}____{self.article}____{self.checked}"
    
    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_dislikes(self):
        return self.dislikes.count()