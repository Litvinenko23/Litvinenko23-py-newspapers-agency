from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.models import Redactor


class RedactorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем 3 экземпляра Redactor для тестов
        number_of_redactors = 3
        for redactor_id in range(number_of_redactors):
            Redactor.objects.create(
                username=f"redactor{redactor_id}",
                password="test_password",
                years_of_experience=redactor_id + 1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/redactors/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("redactor_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("redactor_list"))
        self.assertTemplateUsed(response, "newspaper/redactor_list.html")

    def test_lists_all_redactors(self):
        response = self.client.get(reverse("redactor_list"))
        self.assertEqual(len(response.context["redactor_list"]), 3)


class RedactorDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем экземпляр Redactor для теста
        test_user = get_user_model().objects.create_user(
            username="testuser", password="test_password"
        )
        test_redactor = Redactor.objects.create(
            user=test_user, years_of_experience=2
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/redactors/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("redactor_detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("redactor_detail", args=[1]))
        self.assertTemplateUsed(response, "blog/redactor_detail.html")


class RedactorCreateViewTest(TestCase):
    def setUp(self):
        # Создаем суперпользователя для тестов
        self.user = get_user_model().objects.create_superuser(
            username="testuser", email="testuser@test.com", password="test_password"
        )

    def test_redactor_creation_form(self):
        # Проверяем, что форма создания Redactor возвращает код 200 и использует нужный шаблон
        self.client.force_login(self.user)
        response = self.client.get(reverse("redactor_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/redactor_form.html")

        # Проверяем, что форма корректно сохраняет нового Redactor
        form_data = {
            "username": "new_redactor",
            "password1": "test_password",
            "password2": "test_password",
            "years_of_experience": 5,
        }
        response = self.client.post(reverse("redactor_create"), form_data)
        self.assertRedirects(response, reverse("redactor_list"))
        self.assertEqual(Redactor.objects.count(), 1)
        self.assertEqual(Redactor.objects.first().username, "new_redactor")