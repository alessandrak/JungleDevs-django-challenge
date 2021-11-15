import factory

from faker import Faker

from articles.models import Article
from authors.tests.factory import AuthorFactory

fake = Faker()

class ArticleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Article
    
    category = fake.sentence(nb_words=1)
    title = fake.sentence(nb_words=10)
    summary = fake.paragraph(nb_sentences=5)
    first_paragraph = fake.paragraph(nb_sentences=10)
    body = fake.paragraph(nb_sentences=60)
    author = factory.SubFactory(AuthorFactory)