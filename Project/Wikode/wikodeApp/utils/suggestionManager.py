import random

from django.contrib.auth.models import User
from django.db.models import Count
from enum import Enum
from wikodeApp.models import Activity, Article, FollowRelation, TagRelation, Author
from wikodeApp.utils.articleSuggestionDTO import ArticleSuggestionDTO
from wikodeApp.utils.userSuggestionDTO import UserSuggestionDTO
from wikodeApp.utils.followManager import getFollowerList, getFolloweeList


class UserSuggestionRatings(Enum):
    follower_of_followee = 5
    followers_not_followee = 6
    most_followed = 3
    user_seen_same_article = 7


class ArticleSuggestionRatings(Enum):
    viewed_by_followee = 6
    most_viewed_article = 4
    tagged_by_followee = 8
    recently_tagged = 3
    other_tagged_articles = 9


class SuggestionManager:
    # Limit for suggestion list
    # Upon reach, the manger will stop finding more suggestions
    suggestion_limit = 3
    user_limit = 3

    def __init__(self, user_id):
        owner = User.objects.get(id=user_id)
        self.user_id = user_id
        self.article_list = []
        self.article_id_list = []
        self.user_list = []
        self.user_id_list = []
        self.user_id_list.append(user_id)
        if owner:
            self.owner = owner
            self.followers = getFollowerList(owner)
            self.followees = getFolloweeList(owner)

        for followee in self.followees:
            self.user_id_list.append(followee[0])
    # Ultimate method to get article suggestions
    # returns until "suggestion_limit" is reached.
    # gets random articles if the logic is not sufficient
    def get_article_suggestion(self):

        other_tagged_articles = self.get_other_tagged_articles()
        if other_tagged_articles:
            if isinstance(other_tagged_articles, list):
                for item in other_tagged_articles:
                    self.article_list.append(item)
                    if len(self.article_list) >= self.suggestion_limit:
                        return self.article_list
            else:
                self.article_list.append(other_tagged_articles)


        tagged_articles_from_followee = self.get_tagged_articles_from_followee()
        if tagged_articles_from_followee:
            if isinstance(tagged_articles_from_followee, list):
                for item in tagged_articles_from_followee:
                    self.article_list.append(item)
                    if len(self.article_list) >= self.suggestion_limit:
                        return self.article_list
            else:
                self.article_list.append(tagged_articles_from_followee)

        viewed_article_suggestion_from_followee = self.get_viewed_article_suggestion_from_followee()
        if viewed_article_suggestion_from_followee:
            if isinstance(viewed_article_suggestion_from_followee, list):
                for item in viewed_article_suggestion_from_followee:
                    self.article_list.append(item)
                    if len(self.article_list) >= self.suggestion_limit:
                        return self.article_list
            else:
                self.article_list.append(viewed_article_suggestion_from_followee)


        most_viewed_article = self.get_most_viewed_article()
        if most_viewed_article:
            self.article_list.append(most_viewed_article)
            if len(self.article_list) >= self.suggestion_limit:
                return self.article_list

        recently_tagged_article = self.get_recently_tagged_article()
        if recently_tagged_article:
            self.article_list.append(recently_tagged_article)


        self.get_random_article()
        return self.article_list

    # Ultimate method for user suggestion
    # Returns at least 'user_limit' value
    # gets random user if the logic is not sufficient
    def get_user_suggestion(self):

        users_viewed_same_article = self.get_users_viewed_same_article()
        if users_viewed_same_article:
            self.user_list.append(users_viewed_same_article)
            if len(self.user_list) >= self.user_limit:
                return self.user_list

        followees_of_followees = self.get_followees_of_followees()
        if followees_of_followees:
            self.user_list.append(followees_of_followees)
            if len(self.user_list) >= self.user_limit:
                return self.user_list

        followers_that_is_not_followed = self.get_followers_that_is_not_followed()
        if followers_that_is_not_followed:
            self.user_list.append(followers_that_is_not_followed)
            if len(self.user_list) >= self.user_limit:
                return self.user_list

        most_followed_user = self.get_most_followed_user()
        if most_followed_user:
            self.user_list.append(most_followed_user)
            if len(self.user_list) >= self.user_limit:
                return self.user_list

        if len(User.objects.all()) - len(self.user_id_list) > 2:
            self.get_random_user()

        return self.user_list

    # Gets viewed articles from followee
    # excludes owner's already viewed articles
    def get_viewed_article_suggestion_from_followee(self):
        article_list = self.get_article_id_list_from_followee(activity_type=1)
        return article_list

    # Gets the most viewed article (1)
    # chekcs if the owner has already seen it
    def get_most_viewed_article(self):
        most_common = Activity.objects.filter(activity_type=1, target_type=3)\
            .annotate(mc=Count('target_id'))\
            .order_by('-mc')[0]
        if most_common:
            viewed_article_id_list = self.get_my_viewed_id_list()
            if most_common.target_id in viewed_article_id_list:
                return
            else:

                if most_common.target_id in self.article_id_list:
                    return
                else:
                    article = Article.objects.get(id=most_common.target_id)
                    self.article_id_list.append(most_common.target_id)
                    return article

    # Gets tagged articles from followee
    # excludes owner's already viewed articles
    def get_tagged_articles_from_followee(self):
        article_list = self.get_article_id_list_from_followee(activity_type=6)
        return article_list

    # Gets recently tagged articles from everyone
    # excludes owner's already viewed articles
    def get_recently_tagged_article(self):
        latest_tagged_article_list = []
        tagged_article = Activity.objects.filter(activity_type=6, target_type=3).order_by('-id')
        latest_tagged_article_list.append(tagged_article[0].target_id)
        unique_list = self.substract_viewed_articles(id_list=list(latest_tagged_article_list))
        article_list = []
        for id in unique_list:

            if id in self.article_id_list:
                continue
            else:
                article = Article.objects.get(id=id)
                article_list.append(article)
                self.article_id_list.append(id)
        return article_list

    # Gets other articles that is tagged with same tags
    # excludes owner's already viewed articles
    def get_other_tagged_articles(self):
        my_tags = TagRelation.objects.filter(tagger=self.owner)
        my_tags_id_list = []
        for tag in my_tags:
            if tag.tag_id in my_tags_id_list:
                continue
            else:
                my_tags_id_list.append(tag.tag_id)

        articles_with_my_tags = TagRelation.objects.filter(tag_id__in=my_tags_id_list).exclude(tagger=self.owner)

        article_id_list = []
        for tag in articles_with_my_tags:
            article_id_list.append(tag.article_id)

        article_list = []
        for id in article_id_list:
            if id in self.article_id_list:
                continue
            else:
                article = Article.objects.get(id=id)
                article_list.append(article)
                self.article_id_list.append(id)

        return article_list

    # Returns an article list from followee
    # depending on activity type
    def get_article_id_list_from_followee(self, activity_type):
        article_id_list = []
        if self.followees:
            for followee in self.followees:
                if followee:
                    followee_list = Activity.objects.filter(user_id=followee[0],
                                                            activity_type=activity_type,
                                                            target_type=3)
                    for x in followee_list:
                        if x:
                            article_id_list.append(x.target_id)

        article_id_list = self.substract_viewed_articles(id_list=article_id_list)

        article_list = self.get_articles_from_id_list(id_list=article_id_list)
        return article_list

    # Returns owner's already viewed article list
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

    # Returns an article list, from a given id list
    def get_articles_from_id_list(self, id_list):
        article_list = []
        for id in id_list:
            if id in self.article_id_list:
                continue
            else:
                article = Article.objects.get(id=id)
                article_list.append(article)
                self.article_id_list.append(id)
        return article_list

    # substract an id list from owner's already viewed articles id list
    def substract_viewed_articles(self, id_list):
        viewed_article_id_list = self.get_my_viewed_id_list()
        for viewed_id in viewed_article_id_list:
            if viewed_id in id_list:
                id_list[:] = (value for value in id_list if value != viewed_id)
        return id_list

    # Finds a random article, until the limit is reached
    # excludes viewed articles
    def get_random_article(self):
        viewed_article_id_list = self.get_my_viewed_id_list()
        while (len(self.article_list) < self.suggestion_limit):
            id = random.randrange(200, 20000)
            try:
                article = Article.objects.get(pk=id)
                if article:
                    if id in self.article_id_list:
                        pass
                    else:
                        if id in viewed_article_id_list:
                            pass
                        else:
                            self.article_id_list.append(id)
                            self.article_list.append(article)
                else:
                    pass
            except:
                pass

    # Returns followees of a user
    # who owner follows
    def get_followees_of_followees(self):
        followees_of_followees = []
        for followee in self.followees:
            user = User.objects.get(id=followee[0])
            users_followees = getFolloweeList(user)
            for followee2 in users_followees:
                id = followee2[0]
                if id not in self.user_id_list:
                    followee2_user = User.objects.get(id=id)
                    if followee2_user in followees_of_followees:
                        continue
                    else:
                        self.user_id_list.append(followee2[0])
                        followees_of_followees.append(followee2_user)
                else:
                    continue

        return followees_of_followees

    # Returns followers that owner not follows
    def get_followers_that_is_not_followed(self):
        followers_that_is_not_followed_list = []
        user_list = []
        for follower in self.followers:
            if follower not in self.followees:
                followers_that_is_not_followed_list.append(follower)

        for user in followers_that_is_not_followed_list:
            id = user[0]
            if id in self.user_id_list:
                continue
            else:
                self.user_id_list.append(id)
                user_object = User.objects.get(id=id)
                user_list.append(user_object)

        return user_list

    # Returns the most followed user
    def get_most_followed_user(self):
        most_followed = FollowRelation.objects.all().annotate(mc=Count('followee_id')).order_by('-mc')[0]
        if most_followed:
            id = most_followed.followee_id
            if id in self.user_id_list:
                return
            else:
                self.user_id_list.append(id)
                user_object = User.objects.get(id=id)
                return user_object

    # Returns users that viewed same articles as owner
    def get_users_viewed_same_article(self):
        viewed_articles = Activity.objects.filter(activity_type=1, target_type=3, user_id=self.user_id)
        viewed_article_ids = []
        users = []
        for viewed_article in viewed_articles:
            viewed_article_ids.append(viewed_article.target_id)

        other_views = Activity.objects.filter(activity_type=1, target_type=3, target_id__in=viewed_article_ids)\
            .exclude(user_id=self.user_id)
        for view in other_views:
            id = view.user_id
            if self.check_if_user_is_followee(user_id=id):
                continue
            else:
                self.user_id_list.append(id)
                user_object = User.objects.get(id=id)
                users.append(user_object)

        return users

    # Checks if a user is in the known user list
    def check_if_user_is_followee(self, user_id):
        if user_id in self.user_id_list:
            return True
        else:
            return False

    # Returns a random user, that is not known
    def get_random_user(self):
        while (len(self.user_list) < self.user_limit):
            user = random.choice(User.objects.all().exclude(id=self.user_id))
            if user.id in self.user_id_list:
                continue
            else:
                self.user_id_list.append(user.id)
                self.user_list.append(user)

    def get_article_suggestionDTO_list(self):
        try:
            suggested_articles = self.get_article_suggestion()
            print(suggested_articles)
            article_suggestionDTO_list = []
            for article in suggested_articles:
                if article and not isinstance(article, list):
                    authors = Author.objects.filter(article=article)
                    article_suggestionDTO_list.append(
                        ArticleSuggestionDTO(article.id, article.Title, article.PublicationDate, authors))
                elif isinstance(article, list):
                    for article_item in article:
                        authors = Author.objects.filter(article=article_item)
                        article_suggestionDTO_list.append(
                            ArticleSuggestionDTO(
                                article_item.id, article_item.Title, article_item.PublicationDate, authors
                            ))

            return article_suggestionDTO_list
        except IndexError as error:
            print("Article Suggestion Error = " + str(error))
            return {}

    def get_user_suggestionDTO_list(self):
        try:
            suggested_users = self.get_user_suggestion()
            user_suggestionDTO_list = []
            for user in suggested_users:
                if user and not isinstance(user, list):
                    user_id = user.id
                    follower_count = FollowRelation.objects.filter(followee_id=user_id).count()
                    user_suggestionDTO_list.append(
                        UserSuggestionDTO(user_id, user.first_name, user.last_name, follower_count)
                    )
                elif isinstance(user, list):
                    for user_item in user:
                        user_id = user_item.id
                        follower_count = FollowRelation.objects.filter(followee_id=user_id).count()
                        user_suggestionDTO_list.append(
                            UserSuggestionDTO(user_id, user_item.first_name, user_item.last_name, follower_count)
                        )
            return user_suggestionDTO_list
        except IndexError as error:
            print("User Suggestion Error = " + str(error))
            return {}

