from faker import Faker

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factory import AuthorFactory

User = get_user_model()

class ListAuthorsTestCase(APITestCase):
	"""
	Test case to list all authors
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
		AuthorFactory.create()

	def setUp(self):
		self.client = APIClient()

	def test_list_authors(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.get(reverse('admin-authors-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_list_authors_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.get(reverse('admin-authors-list'))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RetrieveAuthorTestCase(APITestCase):
	"""
	Test case to retrieve an author
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

	def setUp(self):
		self.client = APIClient()

	def test_retrieve_valid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.get(reverse('admin-authors-detail', kwargs={'pk': self.author.pk}))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_invalid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.get(reverse('admin-authors-detail', kwargs={'pk': '123'}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieve_author_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.get(reverse('admin-authors-detail', kwargs={'pk': self.author.pk}))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateNewAuthorTestCase(APITestCase):
	"""
	Test case for creating a new author
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
			'name': Faker().name		
		}
		self.invalid_payload = {
			'name': ''
		}

	def setUp(self):
		self.client = APIClient()

	def test_create_valid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.post(reverse('admin-authors-list'), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.post(reverse('admin-authors-list'), self.invalid_payload)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_author_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.post(reverse('admin-authors-list'), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateAuthorTestCase(APITestCase):
	"""
	Test case for updating an author
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
			'name': Faker().name		
		}
		self.invalid_payload = {
			'name': ''
		}

	def setUp(self):
		self.client = APIClient()
		self.author = AuthorFactory.create()

	def test_update_valid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.put(reverse('admin-authors-detail', kwargs={'pk': self.author.pk}), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_invalid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.put(reverse('admin-authors-detail', kwargs={'pk': self.author.pk}), self.invalid_payload)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_update_author_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.put(reverse('admin-authors-detail', kwargs={'pk': self.author.pk}), self.valid_payload)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteAuthorTestCase(APITestCase):
	"""
	Test case for deleting an author
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

	def setUp(self):
		self.client = APIClient()

	def test_delete_valid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.delete(reverse('admin-authors-detail', kwargs={'pk': self.author.pk}))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_delete_invalid_author(self):
		self.client.force_authenticate(self.admin_user)
		response = self.client.delete(reverse('admin-authors-detail',  kwargs={'pk': '123'}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_delete_author_with_non_admin_user(self):
		self.client.force_authenticate(self.not_admin_user)
		response = self.client.delete(reverse('admin-authors-detail', kwargs={'pk': self.author.pk}))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)