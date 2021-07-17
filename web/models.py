from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


TITLE_CHOICES = (
    ('member', 'member'),
    ('judge', 'judge'),
    ('staff', 'staff'),
    ('pending', 'pending')
)


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Supperuser must be assigned to is_staff")
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be set to True')

        user = self.create_user(email, password=password, **other_fields)
        user.save()
        return user

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide email'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class RRUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, default="Pending")
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'


class Member(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    title = models.CharField(max_length=30, default="Member")
    genre = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='member_images')

    def __str__(self):
        return self.name

class WelcomeBanner(models.Model):
    image = models.ImageField(default="default.img", upload_to='main_image')


class FormsActivation(models.Model):
    member_registration = models.BooleanField(default=True)
    judge_registration = models.BooleanField(default=True)
    entry_form = models.BooleanField(default=True)
    contender_registration = models.BooleanField(default=True)


class BestSolo(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    caption = models.TextField()

    def __str__(self):
        return self.title

class BestDuet(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    caption = models.TextField()

    def __str__(self):
        return self.title

class BestGroupSong(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    caption = models.TextField()

    def __str__(self):
        return self.title
