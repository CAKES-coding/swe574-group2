from django.contrib.auth.models import User
from django.db.models import Count
from enum import Enum
from wikodeApp.models import Activity, Article, Tag, Annotation, FollowRelation
from wikodeApp.utils.activityManager import ActivityManager
from wikodeApp.utils.followManager import getFollowerList, getFolloweeList


class ArticleSuggestionRatings(Enum):
    viewed_by_followee = 6
    most_viewed_article = 4
    tagged_by_followee = 8
    recently_tagged = 3
    other_tagged_articles = 9


class SuggestionManager:

    def __init__(self, user_id):
        owner = User.objects.get(id=user_id)
        self.user_id = user_id
        if owner:
            self.owner = owner
            self.followers = getFollowerList(owner)
            self.followees = getFolloweeList(owner)

    def get_viewed_article_suggestion_from_followee(self):
        article_list = self.get_article_id_list_from_followee(activity_type=1)
        print(article_list)
        return article_list

    def get_most_viewed_article(self):
        most_common = Activity.objects.filter(activity_type=1,target_type=3).annotate(mc=Count('target_id')).order_by('-mc')[0]
        if most_common:
            viewed_article_id_list = self.get_my_viewed_id_list()
            if most_common.target_id in viewed_article_id_list:
                return
            else:
                article = Article.objects.get(id=most_common.target_id)
                return article


    def get_tagged_articles_from_followee(self):
        article_list = self.get_article_id_list_from_followee(activity_type=6)
        return article_list

    def get_article_id_list_from_followee(self, activity_type):
        article_id_list = []
        if self.followees:
            for followee in self.followees:
                if followee:
                    followee_list = Activity.objects.filter(user_id=followee[0], activity_type=activity_type, target_type=3)
                    for x in followee_list:
                        if x:
                            article_id_list.append(x.target_id)

        self.substrct_viewed_articles(id_list=article_id_list)

        article_list = self.get_articles_from_id_list(id_list=article_id_list)
        return article_list

    def get_my_viewed_id_list(self):
        viewed_article_id_list = []
        my_viewed_list = Activity.objects.filter(user_id=self.user_id, activity_type=1, target_type=3)
        for viewed in my_viewed_list:
            if viewed:
                if viewed.target_id in viewed_article_id_list:
                    continue
                else:
                    viewed_article_id_list.append(viewed.target_id)
        return viewed_article_id_list

    def get_articles_from_id_list(self, id_list):
        article_list = []
        for id in id_list:
            article = Article.objects.get(id=id)
            article_list.append(article)
        return article_list

    def substrct_viewed_articles(self, id_list):
        viewed_article_id_list = self.get_my_viewed_id_list()

        for viewed_id in viewed_article_id_list:
            if viewed_id in id_list:
                id_list[:] = (value for value in id_list if value != viewed_id)