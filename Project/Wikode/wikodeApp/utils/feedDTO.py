from django.urls import reverse

from wikodeApp.models import Activity


class Feed:

    def __init__(self, activity_list):

        self.feed = None
        self.activity_list = activity_list

    def create_feed(self):

        feedList = []
        # Here we are creating feeds by considering the activity type
        for eachActivity in self.activity_list:
            # activity type-1 (View activity)
            if eachActivity.activity_type == '1':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                user_url = reverse('getProfilePageOfOtherUser', args=(userID,))
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                article_url =
                feedView = {"userID": userID,
                            "userName": activiyJson.get("actor").get("name"),
                            "articleID": articleID,
                            "articleName": activiyJson.get("object").get("name"),
                            "sentence": "Viewed",
                            "published": activiyJson.get("published")[:10],
                            "publishedTime": activiyJson.get("published")[11:16]
                            }
                feedList.append(feedView)
            # activity type-2 (follow activity)
            if eachActivity.activity_type == '2':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                feedFollow = {"userID": userID,
                              "userName": activiyJson.get("actor").get("name"),
                              "articleID": articleID,
                              "articleName": activiyJson.get("object").get("name"),
                              "sentence": "Followed",
                              "published": activiyJson.get("published")[:10],
                              "publishedTime": activiyJson.get("published")[11:16]
                              }
                feedList.append(feedFollow)
            # activity type-3 (Unfollow activity)
            if eachActivity.activity_type == '3':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                feedUnFollow = {"userID": userID,
                                "userName": activiyJson.get("actor").get("name"),
                                "articleID": articleID,
                                "articleName": activiyJson.get("object").get("name"),
                                "sentence": "Unfollowed",
                                "published": activiyJson.get("published")[:10],
                                "publishedTime": activiyJson.get("published")[11:16]

                                }
                feedList.append(feedUnFollow)
            # activity type-4 (Upvote activity)
            if eachActivity.activity_type == '4':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                feedUpvote = {"userID": userID,
                              "userName": activiyJson.get("actor").get("name"),
                              "articleID": articleID,
                              "articleName": activiyJson.get("object").get("name"),
                              "sentence": "Upvoted",
                              "published": activiyJson.get("published")[:10],
                              "publishedTime": activiyJson.get("published")[11:16]
                              }
                feedList.append(feedUpvote)
            # activity type-5 (Downvote activity)
            if eachActivity.activity_type == '5':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                feedDownvote = {"userID": userID,
                                "userName": activiyJson.get("actor").get("name"),
                                "articleID": articleID,
                                "articleName": activiyJson.get("object").get("name"),
                                "sentence": "Downvoted",
                                "published": activiyJson.get("published")[:10],
                                "publishedTime": activiyJson.get("published")[11:16]
                                }
                feedList.append(feedDownvote)
            # activity type-6 (Tag activity)
            if eachActivity.activity_type == '6':
                activiyJson = eachActivity.activity_JSON
                userID = int(activiyJson.get("actor").get("url").split("/")[-1])
                articleID = int(activiyJson.get("object").get("url").split("/")[-1])
                feedTagged = {"userID": userID,
                              "userName": activiyJson.get("actor").get("name"),
                              "articleID": articleID,
                              "articleName": activiyJson.get("object").get("name"),
                              "sentence": "Tagged",
                              "published": activiyJson.get("published")[:10],
                              "publishedTime": activiyJson.get("published")[11:16]
                              }
                feedList.append(feedTagged)