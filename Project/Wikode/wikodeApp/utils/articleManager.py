from datetime import datetime
from collections.abc import Mapping


class ArticleInfo:
    """
    ArticleInfo class to generate Article, Author, Journal model data from pubMed XML reponse
    Uses articles from PubmedArticleSet/PubmedArticle items
    """
    def __init__(self, article_dict):
        self.article_dict = article_dict

    def getJournal(self):
        journal_info = self.article_dict.get('MedlineCitation').get('Article').get('Journal')
        if journal_info.get('ISSN'):
            journal_dict = {
                'ISSN': journal_info.get('ISSN').get('#text'),
                'Title': journal_info.get('Title'),
                'ISOAbbreviation': journal_info.get('ISOAbbreviation')
                }
            return journal_dict
        else:
            return None

    def getPublicationDate(self):
        journal_info = self.article_dict.get('MedlineCitation').get('Article').get('Journal')
        if journal_info.get('JournalIssue').get('PubDate').get('Day') and journal_info.get('JournalIssue').get('PubDate').get('Month') and journal_info.get('JournalIssue').get('PubDate').get('Year'):
            date_str = journal_info.get('JournalIssue').get('PubDate').get('Year') + '-' + \
                       journal_info.get('JournalIssue').get('PubDate').get('Month') + '-' + \
                       journal_info.get('JournalIssue').get('PubDate').get('Day')
            for fmt in ('%Y-%b-%d', '%Y-%m-%d'):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    pass
            raise ValueError('no valid date format found')

        elif journal_info.get('JournalIssue').get('PubDate').get('Year') and journal_info.get('JournalIssue').get('PubDate').get('Month'):
            date_str = journal_info.get('JournalIssue').get('PubDate').get('Year') + '-' + \
                       journal_info.get('JournalIssue').get('PubDate').get('Month')
            for fmt in ('%Y-%b', '%Y-%m'):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    pass
            raise ValueError('no valid date format found')
        elif journal_info.get('JournalIssue').get('PubDate').get('Year'):
            pub_date = journal_info.get('JournalIssue').get('PubDate').get('Year')
            return datetime.strptime(pub_date, '%Y')
        else:
            return None

    def getAbstract(self):
        abstract_dict = self.article_dict.get('MedlineCitation').get('Article').get('Abstract')
        if abstract_dict:
            abstract_info = abstract_dict.get('AbstractText')
            if type(abstract_info) is str:
                if abstract_info[0] == '[':
                    abstract_text = abstract_info[1:-1]
                else:
                    abstract_text = abstract_info
                return abstract_text
            elif type(abstract_info) is list and abstract_info:
                abstract_text = ''
                for item in abstract_info:
                    if item:
                        if type(item) is str:
                            abstract_text += item + '\n'
                        elif item.get('@Label') and item.get('#text'):
                            abstract_text += item.get('@Label') + '\n' + item.get('#text') + '\n'
                        elif item.get('#text'):
                            abstract_text += item.get('#text') + '\n'
                        else:
                            pass
                return abstract_text
            elif abstract_info:
                return abstract_info.get('#text')
            else:
                return None
        else:
            return None

    def getTitle(self):
        title = self.article_dict.get('MedlineCitation').get('Article').get('ArticleTitle')
        return title

    def getAuthors(self):
        authors_list = self.article_dict.get('MedlineCitation').get('Article').get('AuthorList')
        authors_dict_list = []
        if authors_list:
            for author in authors_list.get('Author'):
                try:
                    if author.get('LastName') and author.get('Initials'):
                        author_dict = {
                            'LastName': author.get('LastName'),
                            'ForeName': author.get('ForeName'),
                            'Initials': author.get('Initials')
                        }

                        identifier = author.get('Identifier')
                        if identifier is not None:
                            identifierText = identifier.get('#text')
                            if not identifierText.startswith('https'):
                                identifierText = "https://orcid.org/" + identifierText
                            author_dict['Identifier'] = identifierText

                        authors_dict_list.append(author_dict)
                except AttributeError:
                    pass
        return authors_dict_list

    def getKeywords(self):
        keywords_data = self.article_dict.get('MedlineCitation').get('KeywordList')
        keywords = []
        if keywords_data:
            for keyword in keywords_data.get('Keyword'):
                if type(keyword) is str:
                    keywords.append(keyword)
                elif keyword.get('#text'):
                    keywords.append(keyword.get('#text'))
                else:
                    pass
        else:
            keywords = None
        return keywords

    def getPMID(self):
        if self.article_dict.get('MedlineCitation').get('PMID'):
            pmid = self.article_dict.get('MedlineCitation').get('PMID').get('#text')
        else:
            pmid = None
        return pmid

    def getTokens(self):
        clean_dict = self.article_dict.get('MedlineCitation')
        clean_dict.pop('PMID', None)
        clean_dict.pop('KeywordList', None)
        clean_dict.get('Article').pop('ArticleTitle', None)
        clean_dict.get('Article').pop('Abstract', None)

        tokens = []

        def iterateArticleData(value):
            if isinstance(value, Mapping):
                for element in value.values():
                    iterateArticleData(element)
            elif type(value) is list:
                for element in value:
                    iterateArticleData(element)
            elif type(value) is str:
                tokens.append(value)

        iterateArticleData(clean_dict)
        return '. '.join(tokens)

    # todo: Get references of the article
    # def getReferences(self):
    # https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pmc&linkname=pmc_refs_pubmed&id=4423606

    # todo: Get how many times article is cited etc.
    # def getArticleMetrics:
    # https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_citedin&id=21876726&id=21876761

