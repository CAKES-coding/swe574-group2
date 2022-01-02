from django.urls import reverse


class UserSuggestionDTO:

    def __init__(self, user_id, first_name, last_name, follower_count):
        self.url = self.create_user_url(user_id)
        self.first_name = first_name
        self.last_name = last_name
        self.follower_count = follower_count

    @staticmethod
    def create_user_url(user_id):
        return reverse('wikodeApp:getProfilePageOfOtherUser', args=(user_id,))
