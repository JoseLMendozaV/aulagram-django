import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import User

from .models import Comment, Like, Post


GIF = (
    b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00"
    b"\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


def image(name="test.gif"):
    return SimpleUploadedFile(name, GIF, content_type="image/gif")


class PostFlowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temporary_media = tempfile.TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.temporary_media.name)
        cls.media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.media_override.disable()
        cls.temporary_media.cleanup()
        super().tearDownClass()

    def setUp(self):
        self.author = User.objects.create_user(
            username="autor", email="autor@example.com", password="test1234"
        )
        self.other = User.objects.create_user(
            username="otro", email="otro@example.com", password="test1234"
        )
        self.post = Post.objects.create(author=self.author, image=image())

    def test_authenticated_user_can_like_and_unlike(self):
        self.client.force_login(self.other)
        url = reverse("posts:like", args=[self.post.pk])
        self.client.post(url)
        self.assertTrue(Like.objects.filter(user=self.other, post=self.post).exists())
        self.client.post(url)
        self.assertFalse(Like.objects.filter(user=self.other, post=self.post).exists())

    def test_user_can_comment(self):
        self.client.force_login(self.other)
        self.client.post(reverse("posts:comment", args=[self.post.pk]), {"body": "Genial"})
        self.assertTrue(Comment.objects.filter(post=self.post, body="Genial").exists())

    def test_non_author_cannot_edit(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("posts:edit", args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_any_post(self):
        admin = User.objects.create_user(
            username="moderador",
            email="moderador@example.com",
            password="test1234",
            role=User.Role.ADMIN,
        )
        self.client.force_login(admin)
        response = self.client.post(reverse("posts:delete", args=[self.post.pk]))
        self.assertRedirects(response, reverse("posts:feed"))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

# Create your tests here.
