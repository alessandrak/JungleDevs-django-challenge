import factory

from faker import Faker

from authors.models import Author


class AuthorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Author
    
    name = Faker().name()
    picture = None
    