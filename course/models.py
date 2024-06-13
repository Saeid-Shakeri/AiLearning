from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User

class Professor(models.Model):
    name = models.CharField(max_length=50)
    degree = models.TextField(null=True,blank=True)
    bio = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(null=True,blank=True,upload_to='media/professor/')
    email = models.EmailField(null=True,blank=True)
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )


    class Meta:
        verbose_name = ("Professor")
        verbose_name_plural = ("Professors")
        

    def __str__(self):
        return f'{self.name}'
    

class ProfRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.PROTECT)
    prof = models.ForeignKey(to=Professor,on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50, help_text="Name of Category")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Parent Category', null=True, blank=True)
    image = models.FileField(null=True, default=None, upload_to='media/category/', blank=True)
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return f"{self.name}"
    

class CategoryRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.PROTECT)
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)


class Course(models.Model):
    category = models.ForeignKey(to=Category,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=50, help_text="Name of Course")
    image = models.FileField(null=True, default=None, upload_to='media/course/course/image/', blank=True)
    file = models.FileField(null=True,blank=True,upload_to='media/course/course/file/')
    body = models.TextField()
    professor = models.ManyToManyField(to=Professor)
    date = models.DateField()
    slug = models.SlugField(unique=True)
    attends = models.PositiveIntegerField(default=0)
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        
    )


    def save(self, *args, **kwargs):
        self.score = round(self.score, 1)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    

    def add_attend(self):
        self.attends += 1
        self.save()
        return True


    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.PROTECT)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)


class Lesson(models.Model):
    name = models.CharField(max_length=50, help_text="Name of Lesson")
    image = models.ImageField(null=True, default=None, upload_to='media/course/lesson/image/', blank=True)
    file = models.FileField(null=True,blank=True,upload_to='media/course/lesson/file/')
    body = models.TextField( null=True, blank=True)
    date = models.DateTimeField()
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE,blank=True,null=True)
    slug = models.SlugField(unique=True)
    video = models.FileField(null=True,blank=True,upload_to='media/course/lesson/video/')
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )



    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f"{self.name} "



class CourseComment(models.Model):
    content = models.CharField(max_length=250, null=True, help_text="Comment text")
    email = models.EmailField()
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )



    class Meta:
        verbose_name = 'Course Comment'
        verbose_name_plural = 'Course Comments'

    def __str__(self):
        return f"Comment: {self.content}"



class Attend(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course,on_delete=models.PROTECT)
    progress = models.DecimalField(max_digits=3,default=0,decimal_places=3)

    
    def __str__(self) -> str:
        return f"{self.user}--{self.course}"

class LessonComment(models.Model):
    content = models.CharField(max_length=250, null=True, help_text="Comment text")
    email = models.EmailField()
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.PROTECT,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )


    class Meta:
        verbose_name = 'Lesson Comment'
        verbose_name_plural = 'Lesson Comments'

    def __str__(self):
        return f"Comment: {self.content}"

