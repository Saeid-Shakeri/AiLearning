from django.utils import timezone
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
    

    def save(self, *args, **kwargs):
        self.score = round(self.score, 1)
        super(Professor, self).save(*args, **kwargs)
    

class ProfRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True)
    prof = models.ForeignKey(to=Professor,on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50, help_text="Name of Category")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Parent Category', null=True, blank=True)
    image = models.FileField(null=True, default=None, upload_to='media/category/', blank=True)
    slug = models.SlugField(unique=True)
    rates = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def calc_score(self):
        n = Course.objects.filter(category=self).count()
        k = Course.objects.filter(category=self)
        a = 0
        for c in k:
            a += c.score

        self.score = a/n 
        self.rates += 1
        self.save()

    def save(self, *args, **kwargs):
        self.score = round(self.score, 1)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    

class CategoryRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)


class Course(models.Model):
    category = models.ForeignKey(to=Category,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50, help_text="Name of Course")
    image = models.FileField(null=True, default=None, upload_to='media/course/course/image/', blank=True)
    file = models.FileField(null=True,blank=True,upload_to='media/course/course/file/')
    body = models.TextField()
    professor = models.ManyToManyField(to=Professor)
    date = models.DateTimeField(default=timezone.now())
    slug = models.SlugField(unique=True)
    attends = models.PositiveIntegerField(default=0)
    rates = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        
    )


    def calc_score(self, avg):
        self.score = round(avg, 1)
        self.save()
        cat = self.category
        cat.calc_score()


    def add_attend(self):
        self.attends += 1
        self.save()
        return True
    


    def save(self, *args, **kwargs):
        self.score = round(self.score, 1)
        super(Course, self).save(*args, **kwargs)



    def __str__(self):
        return f"{self.name}"
    


    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)


class Lesson(models.Model):
    name = models.CharField(max_length=50, help_text="Name of Lesson")
    image = models.ImageField(null=True, default=None, upload_to='media/course/lesson/image/', blank=True)
    file = models.FileField(null=True,blank=True,upload_to='media/course/lesson/file/')
    body = models.TextField( null=True, blank=True)
    date = models.DateTimeField(default=timezone.now())
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


    def save(self, *args, **kwargs):
        self.score = round(self.score, 1)
        super(Lesson, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f"{self.name}____{self.course}"



class LessonRates(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True)
    lesson = models.ForeignKey(to=Lesson,on_delete=models.CASCADE)



# class CourseCommentAnswer(models.Model):
#     # comment = models.ForeignKey(to=CourseComment, on_delete=models.CASCADE)
#     content = models.TextField(help_text="Comment text")
#     email = models.EmailField()
#     name = models.CharField(max_length=50)
#     date_added = models.DateField(auto_now_add=True)
#     rates = models.PositiveIntegerField(default=0)
#     score = models.FloatField(default=0,
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(5),
#         ]
# )


class CourseComment(models.Model):
    content = models.TextField(help_text="Comment text")
    email = models.EmailField()
    name = models.CharField(max_length=50,default='admin')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    # rates = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(to=User,related_name="course_likes",null=True,blank=True)
    checked = models.BooleanField(default=False)
    dislikes = models.ManyToManyField(to=User,related_name="course_dislikes",null=True,blank=True)
    # reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    # score = models.FloatField(default=0,
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(5),
    #     ]
    # )

    class Meta:
        verbose_name = 'Course Comment'
        verbose_name_plural = 'Course Comments'

    def __str__(self):
        return f"{self.name}____{self.course}_____{self.checked}"


    def number_of_likes(self):
        return self.likes.count()
    

    def number_of_dislikes(self):
        return self.dislikes.count()


class Attend(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0,
                validators=[
                    MinValueValidator(0),
                    MaxValueValidator(100),
                ]
    )

    
    def __str__(self) -> str:
        return f"{self.user}-{self.course}"
    




class LessonComment(models.Model):
    content = models.TextField(help_text="Comment text")
    email = models.EmailField()
    name = models.CharField(max_length=50,default='admin')
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE,null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    # rates = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(to=User,related_name="lesson_likes",null=True,blank=True)
    dislikes = models.ManyToManyField(to=User,related_name="lesson_dislikes",null=True,blank=True)
    # reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    # score = models.FloatField(default=0,
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(5),
    #     ]
    # )


    class Meta:
        verbose_name = 'Lesson Comment'
        verbose_name_plural = 'Lesson Comments'

    def __str__(self):
        return f"{self.name}____{self.lesson}____{self.checked}"
    
    def number_of_likes(self):
        return self.likes.count()


    def number_of_dislikes(self):
        return self.dislikes.count()