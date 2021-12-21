from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.fields import JSONField


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
    Identifier = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.ForeName + ' ' + self.LastName


class Keyword(models.Model):
    KeywordText = models.TextField(max_length=64)

    def __str__(self):
        return self.KeywordText


class Tag(models.Model):
    wikiId = models.CharField(max_length=64)
    label = models.CharField(max_length=512)
    description = models.TextField(max_length=1024, null=True)
    aliases = models.TextField(max_length=1024, null=True)
    childTags = models.ManyToManyField("self", related_name='parentTags', symmetrical=False)
    searchIndex = SearchVectorField(null=True)

    def createTSvector(self, *args, **kwargs):
        self.searchIndex = (
                SearchVector('label', weight='A')
                + SearchVector('aliases', weight='B')
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
    Tags = models.ManyToManyField(Tag, through='TagRelation')

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


# Activity Stream 2.0 model
# user_id: the id of the user who makes the activity
# activity_type: activity type form one of the activity_types defined
# target_type: indicates the target type from one of the target_types defined
# target_id: the id of the target object, that is used in the activity
# activity_JSON: the json-ld model regarding the Activity Stream 2.0
class Activity(models.Model):
    activity_types = (('1', 'View'),
                      ('2', 'Follow'),
                      ('3', 'Unfollow'),
                      ('4', 'Like'),
                      ('5', 'Dislike'),
                      ('6', 'Add'))

    target_types = (('1', 'User'),
                    ('2', 'Tag'),
                    ('3', 'Article'))

    user_id = models.IntegerField(max_length=8)
    activity_type = models.CharField(max_length=8, choices=activity_types)
    target_type = models.CharField(max_length=8, choices=target_types)

    target_id = models.IntegerField(max_length=8)

    activity_JSON = JSONField()


class Annotation(models.Model):
    annotation_JSON = JSONField()


class TagRelation(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    fragment = models.TextField(max_length=1024)
    start_index = models.IntegerField(null=True)
    end_index = models.IntegerField(null=True)
    vote_sum = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now, blank=True)
    tagger = models.ForeignKey(User, on_delete=models.CASCADE)


class Vote(models.Model):
    tag_relation = models.ForeignKey(TagRelation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True)


class FollowRelation(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followee', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
