from wikodeApp.models import Article
from functools import reduce
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Sum, Q
from collections import OrderedDict


class SearchResult:
    """
    Gets search terms as a list and return search results as a query set
    """

    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.search_queries = [SearchQuery(term, search_type='phrase') for term in self.search_terms]
        self.article_search_query = reduce(lambda x, y: x & y, self.search_queries)

    def getSearchResults(self):

        ordered_list = self.result_list.\
            values('id', 'PMID', 'Title', 'PublicationDate').\
            annotate(a_rank=SearchRank(F('SearchIndex'), self.article_search_query)).\
            order_by(F('a_rank').desc(nulls_last=True))

        return ordered_list

    def getYearlyArticleCounts(self):
        dates = []

        for date in list(self.result_list.distinct().values('PublicationDate')):
            if date.get('PublicationDate'):
                dates.append(date.get('PublicationDate').year)

        data_dict = {i: dates.count(i) for i in range(min(dates), max(dates)+1)}
        ordered_data = OrderedDict(sorted(data_dict.items()))
        return ordered_data
