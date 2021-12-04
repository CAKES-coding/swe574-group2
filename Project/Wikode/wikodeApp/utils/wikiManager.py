import requests

from wikodeApp.models import TagInheritance, Tag


class WikiEntry:
    """
    WikiEntry class to generate Tag model data from wikidata JSON reponse
    Uses wiki id with Q prefix to fetch entry data
    """
    def __init__(self, wikiID, tag_name=None):
        tag = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids=' + wikiID + '&languages=en&format=json')
        tag_dict = tag.json().get('entities').get(wikiID)
        self.entry_data = tag_dict
        self.tag_name = tag_name

    def getID(self):
        return self.entry_data.get('id')

    def getLabel(self):
        return self.entry_data.get('labels').get('en').get('value')

    def getDescription(self):
        if self.entry_data.get('descriptions'):
            return self.entry_data.get('descriptions').get('en').get('value')
        else:
            return None

    def getAsKnownAs(self):
        if self.entry_data.get('aliases').get('en'):
            alias_list = []
            for alias in self.entry_data.get('aliases').get('en'):
                alias_list.append(alias.get('value'))
            return alias_list
        else:
            return None

    def save(self):
        tag, created = Tag.objects.get_or_create(wikiId=self.getID(), label=self.getLabel(),
                                                 tagName=self.tag_name)

        if created:
            tag.description = self.getDescription()
            tag.aliases = ';'.join(self.getAsKnownAs())
            tag.save()
            tag.createTSvector()

    def saveRelatedWikiItems(self):
        parent_wiki_id = self.entry_data['id']
        related_wiki_id_list = self.getRelatedWikiQidList()
        for relatedWikiId in related_wiki_id_list:
            if not Tag.objects.filter(wikiId=relatedWikiId).exists():
                child_wiki = WikiEntry(relatedWikiId)
                child_tag = Tag.objects.create(wikiId=child_wiki.getID(),
                                               label=child_wiki.getLabel(),
                                               description=child_wiki.getDescription(),
                                               aliases=';'.join(child_wiki.getAsKnownAs())
                                               )

                TagInheritance.objects.create(parentWikiId=parent_wiki_id, childWikiId=relatedWikiId)

    def getRelatedWikiQidList(self):
        related_wiki_id_list = []
        entry_data_claims = self.entry_data['claims']
        wiki_property_list = ['P31', 'P279']
        for wikiProperty in wiki_property_list:
            if entry_data_claims.get(wikiProperty, None):
                for entryDataClaim in entry_data_claims.get(wikiProperty, None):
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
