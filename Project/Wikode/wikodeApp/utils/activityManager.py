import datetime

# the manager that will handle all the activity stream savings to database
from wikodeApp.models import Activity

# Activity Manager will handle all savings to database
# with Activity Model. Call any method related to the activity
# to record an activity.

class ActivityManager:

    # This method saves the 'View' activity to the database.
    # user_id: the id of the user who makes the activity
    # target_type: the type of the target, depends on if the target
    #              is a user, article or tag
    # target_id: the id of the target, correlated with target_type
    def saveViewActivity(user_id, target_type, target_id):

        # TODO: get username from db
        owner_name='Owner'

        current_time = datetime.datetime.now()

        if target_type=='1':
            acitivity_target_type='Person'
            activity_target_url="http://www.wikode.com/wikode/profile/{}".format(target_id)
            acitivity_target_name='PersonName'
        # elif target_type=='2':
        # TODO: when view tags finished, implement the correct tag url:
            #  acitivity_target_type = 'Tag'
            #  activity_target_url = "http://www.wikode.com/wikode/articleDetail/{}".format(target_id)
            #   acitivity_target_type='TagLabel'
        elif target_type=='3':
            acitivity_target_type='Article'
            activity_target_url="http://www.wikode.com/wikode/articleDetail/{}".format(target_id)
            acitivity_target_name = 'ArticleTitle'

        json={
                 "@context": "https://www.w3.org/ns/activitystreams",
                  "summary": "{} viewed {}".format(owner_name, acitivity_target_name),
                  "type": "View",
                  "published": current_time,
                 "actor": {
                      "type": "Person",
                      "id": "http://www.wikode.com/wikode/profile/{}".format(user_id),
                      "name": owner_name,
                      "url": "http://www.wikode.com/wikode/profile/{}".format(user_id)
                 },
                 "object" : {
                      "id": activity_target_url,
                     "type": acitivity_target_type,
                     "url": activity_target_url,
                     "name": acitivity_target_name
                }
        }

        activity=Activity(
            user_id = user_id,
            activity_type = 1,
            target_type = target_type,
            target_id = target_id,
            activity_JSON = json
        )

