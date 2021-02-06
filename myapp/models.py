from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(blank=True, default=12, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(50), MaxValueValidator(500)])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]

    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300)
    province = models.CharField(max_length=2, default="ON")
    registered_courses = models.ManyToManyField(Course, blank=True)
    profile_image = models.ImageField(upload_to='static/myapp/image/', blank=True)
    interested_in = models.ManyToManyField(Topic)

    def courses_registered(self):
        return "\n,".join([c.title for c in self.registered_courses.all()])

    def __str__(self):
        return self.username

class Order(models.Model):
    ORD_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Confirmed'),
        (2, 'On Hold')
    ]

    courses = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, related_name='Student', on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORD_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.student.first_name + " "+ self.student.last_name

    def total_cost(self):
        return sum(course.price for course in self.courses.all())

class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comments = models.TextField(null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.reviewer