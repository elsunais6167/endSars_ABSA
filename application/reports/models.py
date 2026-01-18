from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Reporter', 'Reporter'),
        
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
 
class Incidence(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    select = (
        ('Twitter', 'Twitter'),
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('LinkedIn', 'LinkedIn'),
        ('Others', 'Others'),
    )
    social_media = models.CharField(max_length=50, choices=select) 
    gis_location = models.CharField(max_length=50)
    content = models.TextField(max_length=2500)
    model = models.CharField(max_length=50)
    percentage = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class KnowledgeCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ExpertKnowledge(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(KnowledgeCategory, related_name='knowledge_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class KnowledgeComment(models.Model):
    knowledge = models.ForeignKey(ExpertKnowledge, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.name} on {self.knowledge.title}"
