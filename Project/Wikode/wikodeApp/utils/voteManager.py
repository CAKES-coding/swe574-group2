from wikodeApp.models import Vote, TagRelation, User


# Vote Manager will handle upvote and downvote
# events for article tags.
class VoteManager:

    def __init__(self, user_id):
        self.user_id = user_id

    def upVote(self, tagRelationId):
        if self.isNotUpVoted(tagRelationId):
            tag_relation = TagRelation.objects.get(pk=tagRelationId)
            user = User.objects.get(pk=self.user_id)

            vote = Vote()
            vote.tag_relation = tag_relation
            vote.user = user
            vote.vote = 1
            vote.save()

    def isNotUpVoted(self, tagRelationId):
        vote = Vote.objects.filter(user_id=self.user_id, tag_relation_id=tagRelationId)
        if vote.exists() and vote.vote is 1:
            return False
        return True

