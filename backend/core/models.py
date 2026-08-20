from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.update(is_staff=True, is_superuser=True, role=User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    class Role(models.TextChoices):
        LEARNER = 'learner', 'Learner'
        ADMIN = 'admin', 'Admin'
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.LEARNER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

class Category(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Instructor(TimestampedModel):
    name = models.CharField(max_length=160)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='instructors/', blank=True, null=True)
    def __str__(self): return self.name

class Course(TimestampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self): return self.title

class Enrollment(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['learner', 'course'], name='unique_learner_course')]
        ordering = ['-created_at']
    def __str__(self): return f'{self.learner.email} → {self.course.title}'
