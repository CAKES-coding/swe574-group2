from wikodeApp.models import Article, Author
from functools import reduce
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Q, Value
from collections import OrderedDict
from django.db.models.functions import Concat

class Search:
    """
    Gets search terms as a list and return search results as a query set
    """

    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.search_queries = [SearchQuery(term, search_type='phrase') for term in self.search_terms]
        self.article_search_query = reduce(lambda x, y: x & y, self.search_queries)
        if len(search_terms[0]) > 1:
            self.result_list = Article.objects.filter(Q(SearchIndex=self.article_search_query))
        else:
            self.result_list = Article.objects.all()

    def getSearchResults(self, order_by):
        if order_by == 'relevance':
            ordered_list = self.result_list.\
                values('id', 'PMID', 'Title', 'PublicationDate').\
                annotate(a_rank=SearchRank(F('SearchIndex'), self.article_search_query)).\
                values('id', 'Title', 'PublicationDate').\
                order_by(F('a_rank').desc(nulls_last=True))
        elif order_by == 'date_desc':
            pass
        elif order_by == 'date_asc':
            pass
        else:
            raise ValueError('Cannot sort with given option', order_by + ' is not defined!!')

        return ordered_list

    def filterArticles(self, filters):
        filter_queries = []
        if filters.get('start_date'):
            filter_queries.append(Q(PublicationDate__gte=filters.get('start_date')))

        if filters.get('end_date'):
            filter_queries.append(Q(PublicationDate__lte=filters.get('end_date')))

        if filters.get('journal_field'):
            filter_queries.append(Q(Journal__Title__icontains=filters.get('journal_field')))

        if filters.get('keywords_field'):
            article_set = Article.objects.all()
            for keyword in [term.strip() for term in filters.get('keywords_field').split(';')]:
                article_set = article_set.filter(Keywords__KeywordText__icontains=keyword)
                print(keyword)
            article_is_list = article_set.values('id')
            filter_queries.append(Q(id__in=article_is_list))

        if filters.get('author_field'):
            authors = Author.objects.annotate(search_name=Concat('ForeName', Value(' '), 'LastName'))
            authors_id_list = authors.filter(search_name__icontains=filters.get('author_field'))
            filter_queries.append(Q(Authors__id__in=authors_id_list))

        print(self.search_terms)
        print(filter_queries)
        self.result_list = self.result_list.filter(*filter_queries)

    def getYearlyArticleCounts(self):
        dates = []

        for date in list(self.result_list.distinct().values('PublicationDate')):
            if date.get('PublicationDate'):
                dates.append(date.get('PublicationDate').year)

        data_dict = {i: dates.count(i) for i in range(min(dates), max(dates)+1)}
        ordered_data = OrderedDict(sorted(data_dict.items()))

        return ordered_data
