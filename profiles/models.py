from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

THEMES = [
    ('#0f766e', 'Teal'),
    ('#4f46e5', 'Indigo'),
    ('#be185d', 'Rose'),
    ('#c2410c', 'Orange'),
    ('#15803d', 'Green'),
    ('#334155', 'Slate'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True)
    tagline = models.CharField(max_length=120, blank=True)
    course = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    theme_color = models.CharField(max_length=7, choices=THEMES, default='#0f766e')

    @property
    def display_name(self):
        return self.full_name or self.user.username

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=60)
    level = models.PositiveIntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['-level', 'name']

    def __str__(self):
        return f'{self.name} ({self.level}%)'


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    tech = models.CharField('Technologies used', max_length=100, blank=True)
    link = models.URLField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Photo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or self.image.name


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Every new account automatically gets an empty profile."""
    if created:
        Profile.objects.create(user=instance)
