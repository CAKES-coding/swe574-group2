from django.urls import reverse

from wikodeApp.models import Activity, Tag


class Feed:

    def __init__(self, activity_list):

        self.activity_list = activity_list
        self.feed = self.createFeed()

    def createFeed(self):
        feed_list = []

        # Here we are creating feeds by considering the activity type
        for eachActivity in self.activity_list:
            # activity type-1 (View activity)
            if eachActivity.activity_type == '1':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                user_url = reverse('wikodeApp:getProfilePageOfOtherUser', args=(userID,))
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                target_url = reverse('wikodeApp:articleDetail', args=(articleID,))
                feedView = {"userURL": user_url,
                            "userName": activiyJson.get("actor").get("name"),
                            "targetURL": target_url,
                            "targetName": activiyJson.get("object").get("name"),
                            "sentence": "Viewed",
                            "published": activiyJson.get("published")[:10],
                            "publishedTime": activiyJson.get("published")[11:16]
                            }
                feed_list.append(feedView)
            # activity type-2 (follow activity) and activity type-3 (Unfollow activity)
            if eachActivity.activity_type == '2' or eachActivity.activity_type == '3':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                user_url = reverse('wikodeApp:getProfilePageOfOtherUser', args=(userID,))
                followed_user_id = int(activiyJson.get("object").get("url").split("/")[-1])
                followed_user_url = reverse('wikodeApp:getProfilePageOfOtherUser', args=(followed_user_id,))
                if eachActivity.activity_type == '2':
                    sentence = "Followed"
                else:
                    sentence = "Unfollowed"
                feedFollow = {"userURL": user_url,
                              "userName": activiyJson.get("actor").get("name"),
                              "targetURL": followed_user_url,
                              "targetName": activiyJson.get("object").get("name"),
                              "sentence": sentence,
                              "published": activiyJson.get("published")[:10],
                              "publishedTime": activiyJson.get("published")[11:16]
                              }
                feed_list.append(feedFollow)

            # activity type-4 (Upvote activity) and activity type-5 (Downvote activity)
            if eachActivity.activity_type == '4' or eachActivity.activity_type == '5':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                user_url = reverse('wikodeApp:getProfilePageOfOtherUser', args=(userID,))
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                target_url = reverse('wikodeApp:articleDetail', args=(articleID,))
                if eachActivity.activity_type == '4':
                    sentence = "Upvoted"
                else:
                    sentence = "Downvoted"
                feedUpvote = {"userURL": user_url,
                              "userName": activiyJson.get("actor").get("name"),
                              "targetURL": target_url,
                              "targetName": activiyJson.get("object").get("name"),
                              "sentence": sentence,
                              "published": activiyJson.get("published")[:10],
                              "publishedTime": activiyJson.get("published")[11:16]
                              }
                feed_list.append(feedUpvote)
            # activity type-6 (Tag activity)
            if eachActivity.activity_type == '6':
                activiyJson = eachActivity.activity_JSON
                tag = eachActivity.tag
                tag_name = tag.label
                if tag.wikiId:
                    tag_url = 'https://www.wikidata.org/wiki/' + str(tag.wikiId)
                else:
                    tag_url = '#'
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                user_url = reverse('wikodeApp:getProfilePageOfOtherUser', args=(userID,))
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                target_url = reverse('wikodeApp:articleDetail', args=(articleID,))
                feedTagged = {"userURL": user_url,
                              "userName": activiyJson.get("actor").get("name"),
                              "targetURL": target_url,
                              "targetName": activiyJson.get("object").get("name"),
                              "sentence": "Tagged",
                              "published": activiyJson.get("published")[:10],
                              "publishedTime": activiyJson.get("published")[11:16],
                              "tagName": tag_name,
                              "tagURL": tag_url
                              }
                feed_list.append(feedTagged)

        return feed_list

    def getFeed(self):
        return self.feed
