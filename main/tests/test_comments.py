from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from main import models


class CommentCreateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )

    def test_comment_create(self):
        data = {
            "name": "Jon",
            "email": "jon@wick.com",
            "body": "Content sentence.",
        }
        response = self.client.post(
            reverse("comment_create", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
            data=data,
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(models.Comment.objects.all().count(), 1)
        self.assertEqual(models.Comment.objects.all().first().name, data["name"])
        self.assertEqual(models.Comment.objects.all().first().email, data["email"])
        self.assertEqual(models.Comment.objects.all().first().body, data["body"])
        self.assertEqual(models.Comment.objects.all().first().post, self.post)

        response = self.client.get(
            reverse("post_detail", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "your comment is pending review")


class CommentApprovedCreateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )
        self.comment = models.Comment.objects.create(
            post=self.post,
            name="Jon",
            email="jon@wick.com",
            body="Content sentence.",
            is_approved=True,
        )

    def test_comment_create(self):
        response = self.client.get(
            reverse("post_detail", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jon")
        self.assertContains(response, "Content sentence.")


class CommentNotApprovedCreateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )
        self.comment = models.Comment.objects.create(
            post=self.post,
            name="Jon",
            email="jon@wick.com",
            body="Content sentence.",
            is_approved=False,
        )

    def test_comment_create(self):
        response = self.client.get(
            reverse("post_detail", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Jon")
        self.assertNotContains(response, "Content sentence.")


class CommentNameCreateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )

    def test_comment_create(self):
        data = {
            "name": "Jon",
            "body": "Content sentence.",
        }
        response = self.client.post(
            reverse("comment_create", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Comment.objects.all().count(), 1)
        self.assertEqual(models.Comment.objects.all().first().name, data["name"])
        self.assertEqual(models.Comment.objects.all().first().body, data["body"])
        self.assertEqual(models.Comment.objects.all().first().post, self.post)


class CommentEmailCreateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )

    def test_comment_create(self):
        data = {
            "email": "jon@wick.com",
            "body": "Content sentence.",
        }
        response = self.client.post(
            reverse("comment_create", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Comment.objects.all().count(), 1)
        self.assertEqual(models.Comment.objects.all().first().name, "Anonymous")
        self.assertEqual(models.Comment.objects.all().first().email, data["email"])
        self.assertEqual(models.Comment.objects.all().first().body, data["body"])
        self.assertEqual(models.Comment.objects.all().first().post, self.post)


class CommentAnonCreateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )

    def test_comment_create(self):
        data = {
            "body": "Content sentence.",
        }
        response = self.client.post(
            reverse("comment_create", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Comment.objects.all().count(), 1)
        self.assertEqual(models.Comment.objects.all().first().name, "Anonymous")
        self.assertEqual(models.Comment.objects.all().first().body, data["body"])
        self.assertEqual(models.Comment.objects.all().first().post, self.post)


class CommentNoBodyCreateTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )

    def test_comment_create(self):
        data = {
            "body": "",
        }
        response = self.client.post(
            reverse("comment_create", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Comment.objects.all().count(), 0)


class CommentDisallowedCreateTestCase(TestCase):
    def setUp(self):
        # user.comments_on=False is the default
        self.user = models.User.objects.create(username="alice")
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )

    def test_comment_create(self):
        data = {
            "body": "",
        }
        response = self.client.post(
            reverse("comment_create", args=(self.post.slug,)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Comment.objects.all().count(), 0)


class CommentDeleteTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.client.force_login(self.user)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )
        self.comment = models.Comment.objects.create(
            name="Jon",
            email="jon@wick.com",
            body="Content sentence.",
            post=self.post,
        )

    def test_comment_delete(self):
        response = self.client.post(
            reverse("comment_delete", args=(self.post.slug, self.comment.id)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Comment.objects.all().count(), 0)


class CommentNonOwnerDeleteTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )
        self.comment = models.Comment.objects.create(
            name="Jon",
            email="jon@wick.com",
            body="Content sentence.",
            post=self.post,
        )
        self.non_owner = models.User.objects.create(username="bob")
        self.client.force_login(self.non_owner)

    def test_comment_delete(self):
        response = self.client.post(
            reverse("comment_delete", args=(self.post.slug, self.comment.id)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.Comment.objects.all().count(), 1)


class CommentAnonDeleteTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice", comments_on=True)
        self.post = models.Post.objects.create(
            title="Hello world",
            slug="hello-world",
            owner=self.user,
        )
        self.comment = models.Comment.objects.create(
            name="Jon",
            email="jon@wick.com",
            body="Content sentence.",
            post=self.post,
        )

    def test_comment_delete(self):
        response = self.client.post(
            reverse("comment_delete", args=(self.post.slug, self.comment.id)),
            HTTP_HOST="alice." + settings.CANONICAL_HOST,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.Comment.objects.all().count(), 1)
