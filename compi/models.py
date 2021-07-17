
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from web.models import RRUser

CONSTRAINT_CHOICES = (
    ('g', 'Passing Grade'),
    ('t', 'Top Rank')
)


ENTRY_STATUSES = (
    ('disqualified', 'Disqualified'),
    ('passed', 'Passed'),
    ('failed', 'Failed'),
    ('ongoing', 'ongoing')
)

class Competition(models.Model):
    title = models.CharField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=200)
    is_open = models.BooleanField(null=False, default=False)
    image = models.ImageField(default='default.jpg', upload_to='comp_image')
    submission_date = models.DateTimeField(default=timezone.now)
    result_date = models.DateTimeField(default=timezone.now)
    contender_limit = models.IntegerField()
    constraint = models.CharField(max_length=15, choices=CONSTRAINT_CHOICES, default="Top Rank")
    constraint_value = models.IntegerField()

    def __str__(self):
        return self.title

class Judge(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='judges_images')
    need_comment = models.BooleanField(default=True)
    user = models.ForeignKey(RRUser, null=True, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.competition)

class Criteria(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    competition = models.ForeignKey(Competition, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.competition, self.name)

class Contender(models.Model):
    smule_name = models.CharField(max_length=50)
    line_name = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='contenders_images')
    included = models.BooleanField(default=False)
    competition = models.ForeignKey(Competition, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.smule_name, self.competition)

class Entry(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, choices=ENTRY_STATUSES, default='Ongoing')
    status_comment = models.CharField(max_length=100, null=True)
    contender = models.ForeignKey(Contender, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.title, self.contender) 

class Score(models.Model):
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, null=True, on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.TextField(null=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)