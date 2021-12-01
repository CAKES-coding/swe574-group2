import datetime

# the manager that will handle all the activity stream savings to database
from wikodeApp.models import Activity, Article, RegistrationApplication


# Activity Manager will handle all savings to database
# with Activity Model. Call any method related to the activity
# to record an activity.

class ActivityManager:

    def __init__(self, user_id):
        self.user_id = user_id

    # This method saves the 'View' activity to the database.
    # user_id: the id of the user who makes the activity
    # target_type: the type of the target, depends on if the target
    #              is a user, article or tag
    # target_id: the id of the target, correlated with target_type
    def saveViewActivity(self, target_type, target_id):

        # owner: user who is making the activity
        owner = RegistrationApplication.objects.get(id=self.user_id)
        if isinstance(owner, RegistrationApplication):
            owner_name = owner.name

        current_time=str(datetime.datetime.now().isoformat())

        # target: the object that is being used in the activity by owner
        if target_type == '1':
            target = RegistrationApplication.objects.get(id=target_id)
            if isinstance(target, RegistrationApplication):
                activity_target_type = 'Person'
                activity_target_url = "http://www.wikode.com/wikode/profile/{}".format(target_id)
                activity_target_name = target.name
        # elif target_type=='2':
        # TODO: when view tags finished, implement the correct tag url:
        #  activity_target_type = 'Tag'
        #  activity_target_url = "http://www.wikode.com/wikode/articleDetail/{}".format(target_id)
        #   activity_target_type='TagLabel'
        elif target_type == '3':
            target = Article.objects.get(id=target_id)
            if isinstance(target, Article):
                activity_target_type = 'Article'
                activity_target_url = "http://www.wikode.com/wikode/articleDetail/{}".format(target_id)
                activity_target_name = target.Title

        json = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "{} viewed {}".format(owner_name, activity_target_name),
            "type": "View",
            "published": current_time,
            "actor": {
                "type": "Person",
                "id": "http://www.wikode.com/wikode/profile/{}".format(self.user_id),
                "name": owner_name,
                "url": "http://www.wikode.com/wikode/profile/{}".format(self.user_id)
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
        print('activity saved')
