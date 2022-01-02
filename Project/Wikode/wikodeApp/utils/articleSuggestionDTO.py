from django.urls import reverse


class ArticleSuggestionDTO:

    def __init__(self, article_id, title, published_date, authors):
        self.url = self.create_article_url(article_id)
        self.title = title
        self.published_date = published_date
        self.authors = self.parse_authors(authors)

    @staticmethod
    def create_article_url(article_id):
        return reverse('wikodeApp:articleDetail', args=(article_id,))

    @staticmethod
    def parse_authors(authors):
        author_as_string_list = []
        for author in authors:
            author_as_string = author.ForeName + " " + author.LastName
            author_as_string_list.append(author_as_string)
        return ", ".join(author_as_string_list)

