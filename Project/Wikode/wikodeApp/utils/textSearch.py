from wikodeApp.models import Article, Author, Tag
from functools import reduce
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Q, Value, FloatField
from collections import OrderedDict
from django.db.models.functions import Concat, Cast


class Search:
    """
    Gets search terms as a list and return search results as a query set
    """

    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.search_queries = [SearchQuery(term, search_type='phrase') for term in self.search_terms]
        # For search terms in articles bitwise and
        self.article_search_query = reduce(lambda x, y: x & y, self.search_queries)
        # For search terms in tags bitwise or
        self.tag_search_query = reduce(lambda x, y: x | y, self.search_queries)
        self.related_articles_from_tags = self.getRelatedArticlesByTags()
        if len(search_terms[0]) > 1:
            self.result_list = Article.objects.filter(Q(SearchIndex=self.article_search_query))
        else:
            self.result_list = Article.objects.all()

    def getSearchResults(self, order_by):
        if order_by == 'relevance':
            from_ts = self.result_list. \
                values('id', 'PMID', 'Title', 'PublicationDate'). \
                annotate(a_rank=SearchRank(F('SearchIndex'), self.article_search_query))

            ordered_list = self.related_articles_from_tags.union(from_ts).order_by(F('a_rank').desc(nulls_last=True))

            # ordered_list = results.values('id', 'Title', 'PublicationDate'). \
            #     order_by(F('a_rank').desc(nulls_last=True))

        elif order_by == 'date_desc':
            ordered_list = self.result_list. \
                values('id', 'PMID', 'Title', 'PublicationDate').order_by('-PublicationDate')
        elif order_by == 'date_asc':
            ordered_list = self.result_list. \
                values('id', 'PMID', 'Title', 'PublicationDate').order_by('PublicationDate')
        else:
            raise ValueError('Cannot sort with given option', str(order_by) + ' is not defined!!')

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
            article_is_list = article_set.values('id')
            filter_queries.append(Q(id__in=article_is_list))

        if filters.get('author_field'):
            authors = Author.objects.annotate(search_name=Concat('ForeName', Value(' '), 'LastName'))
            authors_id_list = authors.filter(search_name__icontains=filters.get('author_field'))
            filter_queries.append(Q(Authors__id__in=authors_id_list))

        self.result_list = self.result_list.filter(*filter_queries)

    def getYearlyArticleCounts(self):
        dates = []

        for date in list(self.result_list.distinct().values('PublicationDate')):
            if date.get('PublicationDate'):
                dates.append(date.get('PublicationDate').year)

        data_dict = {i: dates.count(i) for i in range(min(dates), max(dates) + 1)}
        ordered_data = OrderedDict(sorted(data_dict.items()))

        return ordered_data

    def getRelatedArticlesByTags(self):

        main_tags = Tag.objects.filter(Q(searchIndex=self.tag_search_query))
        # Todo: Find dynamic way to rank articles from tags
        articles_from_main_tags = Article.objects.prefetch_related('Tags') \
            .filter(Q(Tags__searchIndex=self.tag_search_query)) \
            .annotate(a_rank=Cast(1, FloatField()))
        parent_tags = Tag.objects.filter(parentTags__in=main_tags)

        # All children of found tags
        articles_from_child_tags = Article.objects.prefetch_related('Tags') \
            .filter(Tags__childTags__in=main_tags) \
            .annotate(a_rank=Cast(0.99, FloatField()))
        articles_from_sibling_tags = Article.objects.prefetch_related('Tags') \
            .filter(Tags__childTags__in=parent_tags) \
            .annotate(a_rank=Cast(0.98, FloatField()))

        # related_articles_from_all_tags = (articles_from_main_tags |
        #                                   articles_from_child_tags |
        #                                   articles_from_sibling_tags) \
        #     .values('id', 'PMID', 'Title', 'PublicationDate', 'a_rank')

        related_articles_from_all_tags = (articles_from_main_tags
                                          .union(articles_from_child_tags)
                                          .union(articles_from_sibling_tags)) \
            .values('id', 'PMID', 'Title', 'PublicationDate', 'a_rank')

        return related_articles_from_all_tags
