import datetime

# the manager that will handle all the activity stream savings to database
from django.contrib.auth.models import User
from wikodeApp.models import Activity, Article, Tag, Annotation


# Activity Manager will handle all savings to database
# with Activity Model. Call any method related to the activity
# to record an activity.

class ActivityManager:
    baseUrl = "http://www.wikode.com/wikode/"

    def __init__(self, user):
        owner = user
        self.user = user
        if owner:
            self.owner = owner

    # This method saves the 'View' activity to the database.
    # user: the user who makes the activity
    # target_type: the type of the target, depends on if the target
    #              is a user, article or tag
    # target_id: the id of the target, correlated with target_type
    def saveViewActivity(self, target_type, target_id):

        if target_type == '1':
            target = self.getTargetAsUser(target_id=target_id)
            if target:
                activity_target_type = 'Person'
                activity_target_url = self.getProfileURL(id=target_id)
                activity_target_name = target.first_name + ' ' + target.last_name
        # elif target_type=='2':
        # TODO: when view tags finished, implement the correct tag url:
        #  activity_target_type = 'Tag'
        #  activity_target_url = "http://www.wikode.com/wikode/articleDetail/{}".format(target_id)
        #   activity_target_type='TagLabel'
        elif target_type == '3':
            target = self.getTargetAsArticle(target_id=target_id)
            if target:
                activity_target_type = 'Article'
                activity_target_url = self.getArticleURL(id=target_id)
                activity_target_name = target.Title
        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} viewed {}".format(self.getOwnerName(), activity_target_name),
            "type": "View",
            "published": self.getCurrentTimeAsISO(),
            "actor": {
                "type": "Person",
                "id": self.getOwnerURL(),
                "name": self.getOwnerName(),
                "url": self.getOwnerURL()
            },
            "object": {
                "id": activity_target_url,
                "type": activity_target_type,
                "url": activity_target_url,
                "name": activity_target_name
            }
        }

        activity = Activity(
            user=self.user,
            activity_type=1,
            target_type=target_type,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    # This method saves a follow activity user -> user
    # follower is the owner of the activity manager
    # target_id: the id of the user who is being followed
    def saveFollowActivity(self, target_id):
        target = self.getTargetAsUser(target_id)
        if target:
            activity_target_type = 'Person'
            activity_target_url = self.getProfileURL(id=target_id)
            activity_target_name = target.first_name + ' ' + target.last_name

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} followed {}".format(self.getOwnerName(), activity_target_name),
            "type": "Follow",
            "published": self.getCurrentTimeAsISO(),
            "actor": {
                "type": "Person",
                "id": self.getOwnerURL(),
                "name": self.getOwnerName(),
                "url": self.getOwnerURL()
            },
            "object": {
                "id": activity_target_url,
                "type": activity_target_type,
                "url": activity_target_url,
                "name": activity_target_name
            }
        }

        activity = Activity(
            user=self.user,
            activity_type=2,
            target_type=1,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    # This method saves an unfollow activity user -> user
    # unfollower is the owner of the activity manager
    # target_id: the id of the user who is being unfollowed
    def saveUnfollowActivity(self, target_id):
        target = self.getTargetAsUser(target_id)
        if target:
            activity_target_type = 'Person'
            activity_target_url = self.getProfileURL(id=target_id)
            activity_target_name = target.first_name + ' ' + target.last_name

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} unfollowed {}".format(self.getOwnerName(), activity_target_name),
            "type": "Unfollow",
            "published": self.getCurrentTimeAsISO(),
            "actor": {
                "type": "Person",
                "id": self.getOwnerURL(),
                "name": self.getOwnerName(),
                "url": self.getOwnerURL()
            },
            "object": {
                "id": activity_target_url,
                "type": activity_target_type,
                "url": activity_target_url,
                "name": activity_target_name
            }
        }

        activity = Activity(
            user=self.user,
            activity_type=3,
            target_type=1,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    # This method saves an upvote activity
    # target_id: the id of the tag which is being upvoted
    def saveUpvoteActivity(self, target_id):
        target = self.getTargetAsTag(target_id)
        if target:
            activity_target_type = 'Note'
            activity_target_url = self.getTagURL(id=target_id)
            activity_target_name = target.label

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} upvoted {}".format(self.getOwnerName(), activity_target_name),
            "type": "Like",
            "published": self.getCurrentTimeAsISO(),
            "actor": {
                "type": "Person",
                "id": self.getOwnerURL(),
                "name": self.getOwnerName(),
                "url": self.getOwnerURL()
            },
            "object": {
                "id": activity_target_url,
                "type": activity_target_type,
                "url": activity_target_url,
                "name": activity_target_name
            }
        }

        activity = Activity(
            user=self.user,
            activity_type=4,
            target_type=2,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    # This method saves a downvote activity
    # target_id: the id of the tag which is being downvoted
    def saveDownvoteActivity(self, target_id):
        target = self.getTargetAsTag(target_id)
        if target:
            activity_target_type = 'Note'
            activity_target_url = self.getTagURL(id=target_id)
            activity_target_name = target.label

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} downvoted {}".format(self.getOwnerName(), activity_target_name),
            "type": "Dislike",
            "published": self.getCurrentTimeAsISO(),
            "actor": {
                "type": "Person",
                "id": self.getOwnerURL(),
                "name": self.getOwnerName(),
                "url": self.getOwnerURL()
            },
            "object": {
                "id": activity_target_url,
                "type": activity_target_type,
                "url": activity_target_url,
                "name": activity_target_name
            }
        }

        activity = Activity(
            user=self.user,
            activity_type=5,
            target_type=2,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    # This method saves a tag activity for a whole article
    # target_id: the id of the article which is being tagged
    # tag_id: the id of the tag which is being used for tagging
    def saveTaggingActivityForArticle(self, target_id, tag_id):
        target = self.getTargetAsArticle(target_id)
        if target:
            activity_target_type = 'Article'
            activity_target_url = self.getTagURL(id=target_id)
            activity_target_name = target.Title

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} tagged {}".format(self.getOwnerName(), activity_target_name),
            "type": "Add",
            "published": self.getCurrentTimeAsISO(),
            "actor": {
                "type": "Person",
                "id": self.getOwnerURL(),
                "name": self.getOwnerName(),
                "url": self.getOwnerURL()
            },
            "tag": {
                "id": self.getTagURL(tag_id)
            },
            "object": {
                "id": activity_target_url,
                "type": activity_target_type,
                "url": activity_target_url,
                "name": activity_target_name
            }
        }

        activity = Activity(
            user=self.user,
            activity_type=6,
            target_type=3,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    # This method saves an annotation activity
    # target_article_id: The id of the article, which has the fragment
    # tag_id: the id of the tag, which is being used for tagging
    # start_index: the beginning index of fragment inside the text
    # end_index: the finishing index of fragment inside the text
    def saveAnnotationActivity(self, target_article_id, tag_id, start_index, end_index):
        tag_object = self.getTargetAsTag(target_id=tag_id)
        json = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": self.getTagURL(id=tag_id),
            "via": "https://www.wikidata.org/wiki/{}".format(tag_object.wikiId),
            "type": "Annotation",
            "body": [
                {
                    "type": "TextualBody",
                    "purpose": "tagging",
                    "value": tag_object.label
                }
            ],
            "target": {
                "source": self.getArticleURL(id=target_article_id),
                "selector": {
                    "type": "TextPositionSelector",
                    "start": start_index,
                    "end": end_index
                }
            }
        }

        annotation = Annotation(
            annotation_JSON=json
        )

        annotation.save()

    def getOwnerName(self):
        return self.owner.first_name + ' ' + self.owner.last_name

    def getOwnerURL(self):
        return self.baseUrl + ("profile/{}".format(self.user.id))

    # returns target as user
    def getTargetAsUser(self, target_id):
        target = User.objects.get(id=target_id)
        if target:
            return target

    def getCurrentTimeAsISO(self):
        return str(datetime.datetime.now().isoformat())

    # returns target as article
    def getTargetAsArticle(self, target_id):
        target = Article.objects.get(id=target_id)
        if target:
            return target

    # returns target as tag
    def getTargetAsTag(self, target_id):
        target = Tag.objects.get(id=target_id)
        if target:
            return target

    def getProfileURL(self, id):
        return self.baseUrl + "profile/{}".format(id)

    def getArticleURL(self, id):
        return self.baseUrl + "articleDetail/{}".format(id)

    def getTagURL(self, id):
        return self.baseUrl + "tag/{}".format(id)
