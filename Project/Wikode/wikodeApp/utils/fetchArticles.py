from django.db.utils import IntegrityError
from Bio import Entrez
import xmltodict
from wikodeApp.utils.articleManager import ArticleInfo
from wikodeApp.models import Journal, Author, Article, Keyword
# from background_task import background
import environ

env = environ.Env()
environ.Env.read_env()


# we might want to make it a background job
# @background(schedule=60)
def createArticles(term, max_article):
    Entrez.api_key = env('ENTREZ_API_KEY')
    Entrez.email = env('ENTREZ_EMAIL')

    search_handle = Entrez.esearch(db="pubmed", term=term, retmax=max_article)
    record = Entrez.read(search_handle)
    search_handle.close()
    id_list = record["IdList"]

    # Todo: check for updates
    existing_articles = list(Article.objects.values_list('PMID', flat=True))
    articles_to_save = list(set(id_list) - set(existing_articles))

    print(str(len(articles_to_save)) + 'articles will be fetched')
    save_counter = 0

    for marker in range(0, len(articles_to_save), 100):
        article_handle = Entrez.efetch(db="pubmed",
                                       id=articles_to_save[marker:marker + 100],
                                       retmode="xml",
                                       rettype="abstract",
                                       retmax=1000)
        articles_xml = article_handle.read()
        articles = xmltodict.parse(articles_xml)
        articles_list = articles.get('PubmedArticleSet').get('PubmedArticle')
        article_handle.close()

        for item in articles_list:

            article_info = ArticleInfo(item)
            if (article_info.getPMID() is not None) and (article_info.getAuthors() is not None) and (article_info.getTitle() is not None) and (article_info.getAbstract() is not None) and (article_info.getPublicationDate() is not None):
                if article_info.getJournal():
                    journal = Journal.objects.get_or_create(**article_info.getJournal())[0]
                else:
                    journal = None

                keywords_list = []
                if article_info.getKeywords():
                    for element in article_info.getKeywords():
                        keyword = Keyword.objects.get_or_create(KeywordText=element)
                        keywords_list.append(keyword[0])

                author_list = []

                for record in article_info.getAuthors():
                    author = Author.objects.get_or_create(**record)
                    author_list.append(author[0])

                article = Article(
                    PMID=article_info.getPMID(),
                    Title=article_info.getTitle(),
                    Abstract=article_info.getAbstract(),
                    PublicationDate=article_info.getPublicationDate(),
                    Journal=journal,
                    Tokens=article_info.getTokens()
                )

                try:
                    article.save()

                    article.createTSvector()

                    if author_list:
                        article.Authors.add(*author_list)

                    if keywords_list:
                        article.Keywords.add(*keywords_list)
                    print('article ' + article.PMID + ' saved.')
                    save_counter = save_counter + 1
                except IntegrityError:
                    print('Article cant be saved')
                    pass
            else:
                print('Article cant be saved')
                pass

        print(str(save_counter) + ' articles saved')
