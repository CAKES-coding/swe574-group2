from wikodeApp.models import FollowRelation
import json


## Create a followee list from Follow relation that the follower id is other_user.id
## List example: [1, 'Can', 'Dayan']
def getFolloweeList(user):
    followee_list = list(
            FollowRelation
                .objects
                .filter(follower_id=user.id)
                .values_list('followee_id', 'followee__first_name', 'followee__last_name')
        )
    return followee_list


## Create a follower list from Follow relation that the followee id is other_user.id
## List example: [1, 'Can', 'Dayan']
def getFollowerList(user):
    follower_list = list(
            FollowRelation
                .objects
                .filter(followee_id=user.id)
                .values_list('follower_id', 'follower__first_name', 'follower__last_name')
        )
    return follower_list
