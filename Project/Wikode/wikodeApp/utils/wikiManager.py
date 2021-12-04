import requests

from wikodeApp.models import TagInheritance


class WikiEntry:
    """
    WikiEntry class to generate Tag model data from wikidata JSON reponse
    Uses wiki id with Q prefix to fetch entry data
    """
    def __init__(self, wikiID):
        tag = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids=' + wikiID + '&languages=en&format=json')
        tag_dict = tag.json().get('entities').get(wikiID)
        self.entry_data = tag_dict

    def getID(self):
        return self.entry_data.get('id')

    def getLabel(self):
        return self.entry_data.get('labels').get('en').get('value')

    def getDescription(self):
        if self.entry_data.get('descriptions'):
            return self.entry_data.get('descriptions').get('en').get('value')
        else:
            return None

    def saveRelatedWikiItems(self):
        parent_wiki_id = self.entry_data['id']
        relatedWikiIdList = self.getRelatedWikiQidList()
        for relatedWikiId in relatedWikiIdList:
            if Tag.objects.filter(wikiId=relatedWikiId).count() == 0:
                tagData = WikiEntry(relatedWikiId)
                Tag.objects.create(wikiId=tagData.getID(), label=tagData.getLabel(),
                                   description=tagData.getDescription())
                TagInheritance.objects.create(parentWikiId=parent_wiki_id, childWikiId=relatedWikiId)

    def getRelatedWikiQidList(self):
        related_wiki_id_list = []
        entry_data_claims = self.entry_data['claims']
        wiki_property_list = ['P31', 'P279']
        for wikiProperty in wiki_property_list:
            if entry_data_claims.get(wikiProperty, None):
                for entryDataClaim in entry_data_claims[wikiProperty]:
                    wiki_id = entryDataClaim['mainsnak']['datavalue']['value']['id']
                    related_wiki_id_list.append(wiki_id)

        return related_wiki_id_list


def getLabelSuggestion(term):
    wiki_set = requests.get('https://www.wikidata.org/w/api.php?action=wbsearchentities&search='
                            + term
                            + '&format=json&language=en&type=item&continue=0')

    suggestions = []
    if wiki_set.json().get('search'):
        for wikipage in wiki_set.json().get('search'):
            page = [wikipage.get('id'),
                    wikipage.get('id') + ': ' + wikipage.get('label') + ' - ' + wikipage.get('description')
                    ]
            suggestions.append(page)

    return suggestions
