from faker import Faker

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factory import ArticleFactory
from articles. models import Article
from authors.tests.factory import AuthorFactory
from articles.serializers import ArticleReadSerializer, ArticleListSerializer, ArticleBasicRetrieveSerializer

User = get_user_model()
fake = Faker()

class ListArticlesTestCase(APITestCase):
	"""
	Test case to list all articles
	"""
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.user = User.objects.create_user(
			'user',
			'user@user.com',
			'password'
		)
		ArticleFactory.create()

	def setUp(self):
		self.client = APIClient()

	def test_list_articles(self):
		self.client.force_authenticate(self.user)
		response = self.client.get(reverse('articles-list'))
		serializer = ArticleListSerializer(Article.objects.all(), many=True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['results'], serializer.data)

	def test_list_articles_with_anonymous_user(self):
		response = self.client.get(reverse('articles-list'))
		serializer = ArticleListSerializer(Article.objects.all(), many=True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['results'], serializer.data)

class RetrieveArticleTestCase(APITestCase):
	"""
	Test case to retrieve an article
	"""
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.user = User.objects.create_user(
			'user',
			'user@user.com',
			'password'
		)
		self.article = ArticleFactory.create()

	def setUp(self):
		self.client = APIClient()

	def test_retrieve_valid_article(self):
		self.client.force_authenticate(self.user)
		response = self.client.get(reverse('articles-detail', kwargs={'pk': self.article.pk}))
		serializer = ArticleReadSerializer(self.article)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, serializer.data)

	def test_retrieve_invalid_article(self):
		self.client.force_authenticate(self.user)
		response = self.client.get(reverse('articles-detail', kwargs={'pk': '123'}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieve_valid_article_with_anonymous_user(self):
		response = self.client.get(reverse('articles-detail', kwargs={'pk': self.article.pk}))
		serializer = ArticleBasicRetrieveSerializer(self.article)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, serializer.data)


class ListArticlesAdminTestCase(APITestCase):
	"""
	Test case to list all articles in Admin API
	"""
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.admin_user = User.objects.create_superuser(
			'admin',
			'admin@admin.com',
			'password'
		)
		self.not_admin_user = User.objects.create_user(
			'user',
			'user@user.com',
			'password'
		)
		ArticleFactory.create()

	def setUp(self):
		self.client = APIClient()

	def test_list_articles(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.get(reverse('admin-articles-list'))
		serializer = ArticleReadSerializer(Article.objects.all(), many=True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['results'], serializer.data)

	def test_list_articles_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.get(reverse('admin-articles-list'))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RetrieveArticleAdminTestCase(APITestCase):
	"""
	Test case to retrieve an article in Admin API
	"""
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.admin_user = User.objects.create_superuser(
			'admin',
			'admin@admin.com',
			'password'
		)
		self.not_admin_user = User.objects.create_user(
			'user',
			'user@user.com',
			'password'
		)
		self.article = ArticleFactory.create()

	def setUp(self):
		self.client = APIClient()

	def test_retrieve_valid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.get(reverse('admin-articles-detail', kwargs={'pk': self.article.pk}))
		serializer = ArticleReadSerializer(self.article)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, serializer.data)

	def test_retrieve_invalid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.get(reverse('admin-articles-detail', kwargs={'pk': '123'}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieve_article_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.get(reverse('admin-articles-detail', kwargs={'pk': self.article.pk}))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CreateNewArticleTestCase(APITestCase):
	"""
	Test case for creating a new article
	"""
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.admin_user = User.objects.create_superuser(
			'admin',
			'admin@admin.com',
			'password'
		)
		self.not_admin_user = User.objects.create_user(
			'user',
			'user@user.com',
			'password'
		)
		self.author = AuthorFactory.create()
		self.valid_payload = {
			'category': fake.sentence(nb_words=1),
			'title': fake.sentence(nb_words=10),
			'summary': fake.paragraph(nb_sentences=5),
			'first_paragraph': fake.paragraph(nb_sentences=10),
			'body': fake.paragraph(nb_sentences=60),
			'author': self.author.pk
		}
		self.invalid_payload = {
			'category': '',
			'title': '',
			'author': '123'
		}

	def setUp(self):
		self.client = APIClient()

	def test_create_valid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.post(reverse('admin-articles-list'), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.post(reverse('admin-articles-list'), self.invalid_payload)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_article_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.post(reverse('admin-articles-list'), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateArticleTestCase(APITestCase):
	"""
	Test case for updating an article
	"""
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.admin_user = User.objects.create_superuser(
			'admin',
			'admin@admin.com',
			'password'
		)
		self.not_admin_user = User.objects.create_user(
			'user',
			'user@user.com',
			'password'
		)
		self.valid_payload = {
			'title': 'novo titulo',	
		}
		self.invalid_payload = {
			'title': ''
		}

	def setUp(self):
		self.client = APIClient()
		self.article = ArticleFactory.create()

	def test_update_valid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.patch(reverse('admin-articles-detail', kwargs={'pk': self.article.pk}), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_invalid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.patch(reverse('admin-articles-detail', kwargs={'pk': self.article.pk}), self.invalid_payload)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_update_article_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.patch(reverse('admin-articles-detail', kwargs={'pk': self.article.pk}), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteArticleTestCase(APITestCase):
	"""
	Test case for deleting an article
	"""
	@classmethod
	def setUpClass(self):
		super().setUpClass()
		self.admin_user = User.objects.create_superuser(
			'admin',
			'admin@admin.com',
			'password'
		)
		self.not_admin_user = User.objects.create_user(
			'user',
			'user@user.com',
			'password'
		)
		self.article = ArticleFactory.create()

	def setUp(self):
		self.client = APIClient()

	def test_delete_valid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.delete(reverse('admin-articles-detail', kwargs={'pk': self.article.pk}))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_delete_invalid_article(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.delete(reverse('admin-articles-detail',  kwargs={'pk': '123'}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_delete_article_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.delete(reverse('admin-articles-detail', kwargs={'pk': self.article.pk}))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)