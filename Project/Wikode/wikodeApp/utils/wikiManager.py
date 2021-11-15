import requests


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
