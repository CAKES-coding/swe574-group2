from django.db.models import Sum

from wikodeApp.models import Vote, TagRelation, User
from enum import Enum


# Vote Manager will handle upvote and downvote
# events for article tags.
class VoteManager:

    def __init__(self, user_id):
        self.user_id = user_id

    def upVote(self, tag_relation_id):
        self.createVote(tag_relation_id, VoteEnum.UPVOTED.value)

        vote = self.getVote(tag_relation_id)[0]
        if vote.value == VoteEnum.NOTR.value:
            self.updateVote(vote, VoteEnum.UPVOTED.value)
        elif vote.value == VoteEnum.DOWNVOTED.value:
            self.updateVote(vote, VoteEnum.NOTR.value)

    def downVote(self, tag_relation_id):
        self.createVote(tag_relation_id, VoteEnum.DOWNVOTED.value)

        vote = self.getVote(tag_relation_id)[0]
        if vote.value == VoteEnum.NOTR.value:
            self.updateVote(vote, VoteEnum.DOWNVOTED.value)
        elif vote.value == VoteEnum.UPVOTED.value:
            self.updateVote(vote, VoteEnum.NOTR.value)

    def createVote(self, tag_relation_id, value):
        vote = self.getVote(tag_relation_id)
        if not vote.exists():
            tag_relation = TagRelation.objects.get(pk=tag_relation_id)
            user = User.objects.get(pk=self.user_id)

            vote = Vote()
            vote.tag_relation = tag_relation
            vote.user = user
            vote.value = value
            vote.save()

    def updateVote(self, vote, value):
        vote.value = value
        vote.save()

    def getVote(self, tag_relation_id):
        return Vote.objects.filter(user_id=self.user_id, tag_relation_id=tag_relation_id)

    def getVoteSum(self, tag_relation_id):
        votes = Vote.objects.filter(tag_relation_id=tag_relation_id)
        return votes.aggregate(values=Sum('value'))['values']

class VoteEnum(Enum):
    UPVOTED = 1
    NOTR = 0
    DOWNVOTED = -1
