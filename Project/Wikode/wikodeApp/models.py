from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField, SearchVector


class RegistrationApplication(models.Model):
    applicationStatuses = (
        ('1', 'New'),
        ('2', 'Approved'),
        ('3', 'Rejected')
    )

    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()
    applicationText = models.TextField(max_length=512)
    applicationDate = models.DateTimeField(default=timezone.now)
    applicationStatus = models.CharField(max_length=20, choices=applicationStatuses, default='1')


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registrationApplication = models.ForeignKey(RegistrationApplication, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Journal(models.Model):
    ISSN = models.CharField(max_length=16)
    Title = models.CharField(max_length=256)
    ISOAbbreviation = models.CharField(max_length=256)

    def __str__(self):
        return self.Title


class Author(models.Model):
    LastName = models.CharField(max_length=128)
    ForeName = models.CharField(max_length=128, null=True)
    Initials = models.CharField(max_length=32)

    def __str__(self):
        return self.ForeName + ' ' + self.LastName


class Keyword(models.Model):
    KeywordText = models.TextField(max_length=64)

    def __str__(self):
        return self.KeywordText


class Tag(models.Model):
    tagName = models.CharField(max_length=64, default='noname')
    wikiId = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True)
    # Maybe an array field for tokens?
    tokens = models.TextField(max_length=1024, null=True)
    searchIndex = SearchVectorField(null=True)

    def createTSvector(self, *args, **kwargs):
        self.searchIndex = (
                SearchVector('label', weight='A')
                + SearchVector('tokens', weight='B')
                + SearchVector('description', weight='C')
        )
        super().save(*args, **kwargs)


class Article(models.Model):
    PMID = models.CharField(max_length=16)
    Title = models.TextField(max_length=512)
    Abstract = models.TextField(max_length=5000, null=True)
    PublicationDate = models.DateField(null=True)

    Journal = models.ForeignKey(Journal, on_delete=models.PROTECT, null=True)
    Keywords = models.ManyToManyField(Keyword)
    Authors = models.ManyToManyField(Author)
    Tags = models.ManyToManyField(Tag)

    Tokens = models.TextField(max_length=100000)
    SearchIndex = SearchVectorField(null=True)

    def createTSvector(self, *args, **kwargs):
        self.SearchIndex = (
                SearchVector('PMID', weight='A')
                + SearchVector('Title', weight='A')
                + SearchVector('Abstract', weight='B')
                + SearchVector('Tokens', weight='C')
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Title
