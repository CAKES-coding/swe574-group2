import datetime

# the manager that will handle all the activity stream savings to database
from wikodeApp.models import Activity, Article, RegistrationApplication, Tag


# Activity Manager will handle all savings to database
# with Activity Model. Call any method related to the activity
# to record an activity.

class ActivityManager:

    def __init__(self, user_id):
        owner = RegistrationApplication.objects.get(id=user_id)
        self.user_id = user_id
        if isinstance(owner, RegistrationApplication):
            self.owner=owner

    # This method saves the 'View' activity to the database.
    # user_id: the id of the user who makes the activity
    # target_type: the type of the target, depends on if the target
    #              is a user, article or tag
    # target_id: the id of the target, correlated with target_type
    def saveViewActivity(self, target_type, target_id):

        if target_type == '1':
            target = self.getTargetAsUser(target_id=target_id)
            if isinstance(target, RegistrationApplication):
                activity_target_type = 'Person'
                activity_target_url = self.getProfileURL(id=target_id)
                activity_target_name = target.name
        # elif target_type=='2':
        # TODO: when view tags finished, implement the correct tag url:
        #  activity_target_type = 'Tag'
        #  activity_target_url = "http://www.wikode.com/wikode/articleDetail/{}".format(target_id)
        #   activity_target_type='TagLabel'
        elif target_type == '3':
            target = self.getTargetAsArticle(target_id=target_id)
            if isinstance(target, Article):
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
            user_id=self.user_id,
            activity_type=1,
            target_type=target_type,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    def saveFollowActivity(self, target_id):
        target=self.getTargetAsUser(target_id)
        if isinstance(target, RegistrationApplication):
            activity_target_type = 'Person'
            activity_target_url = self.getProfileURL(id=target_id)
            activity_target_name = target.name

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
            user_id=self.user_id,
            activity_type=2,
            target_type=1,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    def saveUnfollowActivity(self, target_id):
        target = self.getTargetAsUser(target_id)
        if isinstance(target, RegistrationApplication):
            activity_target_type = 'Person'
            activity_target_url = self.getProfileURL(id=target_id)
            activity_target_name = target.name

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
            user_id=self.user_id,
            activity_type=3,
            target_type=1,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    def saveUpvoteActivity(self, target_id):
        target = self.getTargetAsTag(target_id)
        if isinstance(target, Tag):
            activity_target_type = 'Note'
            activity_target_url = self.getTagURL(id=target_id)
            activity_target_name = target.tagName

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} upvoted {}".format(self.getOwnerName(), activity_target_name),
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
            user_id=self.user_id,
            activity_type=4,
            target_type=2,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    def saveDownvoteActivity(self, target_id):
        target = self.getTargetAsTag(target_id)
        if isinstance(target, Tag):
            activity_target_type = 'Note'
            activity_target_url = self.getTagURL(id=target_id)
            activity_target_name = target.tagName

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} downvoted {}".format(self.getOwnerName(), activity_target_name),
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
            user_id=self.user_id,
            activity_type=5,
            target_type=2,
            target_id=target_id,
            activity_JSON=json
        )
        activity.save()

    def getOwnerName(self):
        return self.owner.name

    def getOwnerURL(self):
        return self.getBaseURL() + ("/profile/{}".format(self.user_id))

    # returns target as user
    def getTargetAsUser(self, target_id):
        target = RegistrationApplication.objects.get(id=target_id)
        if isinstance(target, RegistrationApplication):
            return target

    def getCurrentTimeAsISO(self):
       return str(datetime.datetime.now().isoformat())

    # returns target as article
    def getTargetAsArticle(self, target_id):
        target = Article.objects.get(id=target_id)
        if isinstance(target, Article):
            return target

    # returns target as tag
    def getTargetAsTag(self, target_id):
        target = Tag.objects.get(id=target_id)
        if isinstance(target, Tag):
            return target

    def getBaseURL(self):
        return "http://www.wikode.com/wikode/"

    def getProfileURL(self, id):
        return self.getBaseURL() + "profile/{}".format(id)

    def getArticleURL(self, id):
        return self.getBaseURL() + "articleDetail/{}".format(id)

    def getTagURL(self, id):
        return self.getBaseURL() + "tag/{}".format(id)