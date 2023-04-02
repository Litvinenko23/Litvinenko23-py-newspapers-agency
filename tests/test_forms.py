from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from newspaper.models import Redactor, Topic, Newspaper
from newspaper.forms import RedactorCreationForm, NewspaperForm


class NewspaperFormTests(TestCase):

    def test_newspaper_create_form_valid_data(self):
        user = Redactor.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        data = {
            "title": "Test newspaper title",
            "content": "Test newspaper content",
            "published_date": timezone.now(),
        }
        form = NewspaperForm(data=data)
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse("newspaper_create"), data=data)
        self.assertEqual(response.status_code, 302)  # Redirects to detail view
        self.assertEqual(Newspaper.objects.count(), 1)
        newspaper = Newspaper.objects.first()
        self.assertEqual(newspaper.title, "Test newspaper title")
        self.assertEqual(newspaper.content, "Test newspaper content")

    def test_newspaper_create_form_invalid_data(self):
        user = Redactor.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        data = {
            "title": "",
            "content": "",
            "published_date": timezone.now(),
        }
        form = NewspaperForm(data=data)
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse("newspaper_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "title", "This field is required.")
        self.assertFormError(response, "form", "content", "This field is required.")
        self.assertEqual(Newspaper.objects.count(), 0)

    def test_newspaper_update_form_valid_data(self):
        user = Redactor.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        newspaper = Newspaper.objects.create(
            title="Test newspaper title",
            content="Test newspaper content",
            published_date=timezone.now(),
        )

        data = {
            "title": "Updated newspaper title",
            "content": "Updated newspaper content",
            "published_date": timezone.now(),
        }
        form = NewspaperForm(data=data, instance=newspaper)
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse("newspaper_update", args=[newspaper.pk]), data=data)
        self.assertEqual(response.status_code, 302)  # Redirects to detail view
        newspaper.refresh_from_db()
        self.assertEqual(newspaper.title, "Updated newspaper title")
        self.assertEqual(newspaper.content, "Updated newspaper content")
