from django.test import TestCase
from django.urls import reverse

from .models import Profile, User


class AuthenticationTests(TestCase):
    def test_register_creates_member_and_profile(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "ana",
                "email": "ana@example.com",
                "first_name": "Ana",
                "last_name": "Perez",
                "password1": "ClaveSegura-2026",
                "password2": "ClaveSegura-2026",
            },
        )
        user = User.objects.get(username="ana")
        self.assertRedirects(response, reverse("accounts:profile_edit"))
        self.assertEqual(user.role, User.Role.MEMBER)
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_anonymous_user_is_redirected_from_profile_edit(self):
        response = self.client.get(reverse("accounts:profile_edit"))
        self.assertRedirects(
            response, f"{reverse('accounts:login')}?next={reverse('accounts:profile_edit')}"
        )


class RolePermissionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin", email="admin@example.com", password="test1234", role=User.Role.ADMIN
        )
        self.member = User.objects.create_user(
            username="member", email="member@example.com", password="test1234"
        )

    def test_member_cannot_open_user_management(self):
        self.client.force_login(self.member)
        response = self.client.get(reverse("accounts:user_list"))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_change_a_role(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("accounts:role_update", args=[self.member.pk]),
            {"role": User.Role.CREATOR},
        )
        self.member.refresh_from_db()
        self.assertRedirects(response, reverse("accounts:user_list"))
        self.assertEqual(self.member.role, User.Role.CREATOR)

# Create your tests here.
