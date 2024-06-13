from django.db import models
 

class Professor(models.Model):
    name = models.CharField(max_length=50)
    degree = models.TextField(null=True,blank=True)
    bio = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(null=True,blank=True,upload_to='media/professor/')
    score = models.PositiveIntegerField(default=0)
    email = models.EmailField(null=True,blank=True)

    class Meta:
        verbose_name = ("Professor")
        verbose_name_plural = ("Professors")
        

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, help_text="Name of Category")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Parent Category', null=True, blank=True)
    image = models.FileField(null=True, default=None, upload_to='media/category/', blank=True)
    score = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    category = models.ForeignKey(to=Category,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=50, help_text="Name of Course")
    image = models.FileField(null=True, default=None, upload_to='media/course/course/image/', blank=True)
    file = models.FileField(null=True,blank=True,upload_to='media/course/course/file/')
    body = models.TextField()
    professor = models.ManyToManyField(to=Professor)
    score = models.PositiveIntegerField(default=0)
    date = models.DateField()
    slug = models.SlugField(unique=True)
    attends = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
    

    def add_attend(self):
        self.attends += 1
        self.save()
        return True


    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Lesson(models.Model):
    name = models.CharField(max_length=50, help_text="Name of Lesson")
    image = models.ImageField(null=True, default=None, upload_to='media/course/lesson/image/', blank=True)
    file = models.FileField(null=True,blank=True,upload_to='media/course/lesson/file/')
    body = models.TextField( null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE,blank=True,null=True)
    slug = models.SlugField(unique=True)
    video = models.FileField(null=True,blank=True,upload_to='media/course/lesson/video/')


    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f"{self.name} "



class CourseComment(models.Model):
    content = models.CharField(max_length=250, null=True, help_text="Comment text")
    email = models.EmailField()
    score = models.PositiveIntegerField(default=0)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Course Comment'
        verbose_name_plural = 'Course Comments'

    def __str__(self):
        return f"Comment: {self.content}"



class LessonComment(models.Model):
    content = models.CharField(max_length=250, null=True, help_text="Comment text")
    email = models.EmailField()
    score = models.PositiveIntegerField(default=0)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.PROTECT,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Lesson Comment'
        verbose_name_plural = 'Lesson Comments'

    def __str__(self):
        return f"Comment: {self.content}"


