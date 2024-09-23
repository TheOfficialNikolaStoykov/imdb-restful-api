from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase

from media_app.api.views import ReviewList

from .models import *


class StreamingPlatformTestCase(APITestCase):
    """
    Test case for streaming platform endpoints.
    """

    def setUp(self):
        """
        Set up test data and authentication for the test user.
        """
        self.user = User.objects.create_user(username="testcase", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.streaming_platform = StreamingPlatform.objects.create(
            name="Test",
            about="Test",
            website="https://www.test.com"
        )

    def test_streaming_platform_create(self):
        """
        Test that streaming platform creation is forbidden for non-admin users.
        """
        data = {
            "name": "Test",
            "about": "Test",
            "website": "https://test.com"
        }
        
        response = self.client.post(reverse("streaming_platform-list"), data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):
        """
        Test listing streaming platforms.
        """
        response = self.client.get(reverse("streaming_platform-list"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streaming_platform_detail(self):
        """
        Test retrieving a single streaming platform by its ID.
        """
        response = self.client.get(reverse("streaming_platform-detail", args=(self.streaming_platform.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MediaTestCase(APITestCase):
    """
    Test case for media endpoints.
    """

    def setUp(self):
        """
        Set up test data, including users and media objects.
        """
        self.user = User.objects.create_user(username="test_user", password="password")
        self.admin_user = User.objects.create_superuser(username="test_user_admin", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.streaming_platform = StreamingPlatform.objects.create(
            name="Test",
            about="Test",
            website="https://www.test.com"
        )
        self.media_object = Media.objects.create(
            title="Test",
            storyline="Test",
            streaming_platform=self.streaming_platform,
            user_rating=4,
            active=True
        )

    def test_media_create_201(self):
        """
        Test that an admin can create a new media object.
        """
        self.client.login(username="test_user_admin", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "title": "New Test Media",
            "storyline": "This is a test media",
            "streaming_platform": self.streaming_platform.id,
            "user_rating": 4,
            "active": True
        }

        response = self.client.post(reverse("media-list"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_media_create_400(self):
        """
        Test that media creation fails with incomplete data.
        """
        self.client.login(username="test_user_admin", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "title": "New Test Media",
            "storyline": "This is a test media",
            "streaming_platform": self.streaming_platform.id,
            "active": True
        }

        response = self.client.post(reverse("media-list"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_media_list(self):
        """
        Test listing all media.
        """
        response = self.client.get(reverse("media-list"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_media_detail_get(self):
        """
        Test retrieving a single media object by its ID.
        """
        response = self.client.get(reverse("media-detail", args=(self.media_object.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_media_detail_404(self):
        """
        Test retrieving a media object that does not exist.
        """
        response = self.client.get(reverse("media-detail", args=(9999,)))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_media_detail_put(self):
        """
        Test updating a media object.
        """
        self.client.login(username="test_user_admin", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "title": "Test - Edited",
            "storyline": "Test",
            "streaming_platform": self.streaming_platform.id,
            "user_rating": 4,
            "active": True
        }

        response = self.client.put(reverse("media-detail", args=(self.media_object.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_media_detail_put_400(self):
        """
        Test that updating a media object with invalid data fails.
        """
        self.client.login(username="test_user_admin", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "title": "Test",
            "storyline": "Test",
            "streaming_platform": 999,
            "user_rating": 4,
            "active": True,
        }

        response = self.client.put(reverse("media-detail", args=(self.media_object.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_media_detail_delete(self):
        """
        Test deleting a media object.
        """
        self.client.login(username="test_user_admin", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(reverse("media-detail", args=(self.media_object.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewTestCase(APITestCase):
    """
    Test case for review endpoints.
    """

    def setUp(self):
        """
        Set up test data, including users, media objects, and reviews.
        """
        self.user = User.objects.create_user(username="testcase", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.factory = APIRequestFactory()
        self.streaming_platform = StreamingPlatform.objects.create(
            name="Test",
            about="Test",
            website="https://www.test.com"
        )
        self.media_object = Media.objects.create(
            title="Test",
            storyline="Test",
            streaming_platform=self.streaming_platform,
            user_rating=4,
            active=True
        )
        self.media_object_2 = Media.objects.create(
            title="Test",
            storyline="Test",
            streaming_platform=self.streaming_platform,
            user_rating=4,
            active=True
        )
        self.review = Review.objects.create(
            reviewer=self.user,
            rating=2,
            description="Test",
            media=self.media_object_2,
            active=True
        )

    def test_review_create(self):
        """
        Test creating a review for a media object.
        """
        data = {
            "reviewer": self.user.id,
            "rating": 1,
            "description": "Test",
            "media": self.media_object.id,
            "active": True
        }

        response = self.client.post(reverse("review-create", args=(self.media_object.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse("review-create", args=(self.media_object.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauthneticated(self):
        """
        Test that unauthenticated users cannot create reviews.
        """
        data = {
            "reviewer": self.user.id,
            "rating": 1,
            "description": "Test",
            "media": self.media_object.id,
            "active": True
        }

        self.client.force_authenticate(user=None)
        
        response = self.client.get(reverse("review-create", args=(self.media_object.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        """
        Test updating a review.
        """
        data = {
            "reviewer": self.user.id,
            "rating": 3,
            "description": "Test - updated",
            "media": self.media_object.id,
            "active": True
        }

        response = self.client.put(reverse("review-detail", args=(self.review.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        """
        Test listing all reviews for a media object.
        """
        response = self.client.get(reverse("review-list", args=(self.media_object.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_swagger_fake_view_returns_empty_queryset(self):
        """
        Test that the get_queryset method returns an empty queryset 
        when accessed by Swagger (i.e., swagger_fake_view is True).
        """

        request = self.factory.get("/api/reviews/")
        
        view = ReviewList()
        view.request = request
        view.kwargs = {"pk": 1}
        setattr(view, "swagger_fake_view", True)

        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 0)

    def test_review_detail(self):
        """
        Test retrieving a single review by its ID.
        """
        response = self.client.get(reverse("review-detail", args=(self.review.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        """
        Test listing reviews by a specific user.
        """
        response = self.client.get("/api/media/reviews/user/?username=" + self.user.username)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IsAdminOrReadOnlyPermissionTestCase(APITestCase):
    """
    Test case for the IsAdminOrReadOnly permission.
    """

    def setUp(self):
        """
        Set up test data, including regular and admin users, and a streaming platform.
        """
        self.user = User.objects.create_user(username="test_user", password="password")
        self.admin_user = User.objects.create_superuser(username="test_user_admin", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.streaming_platform = StreamingPlatform.objects.create(
            name="Test",
            about="Test",
            website="https://test.com"
        )

    def test_read_only_access(self):
        """
        Test that regular users can only read streaming platform data.
        """
        response = self.client.get(reverse("streaming_platform-detail", args=(self.streaming_platform.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "name": "Test - Edited",
            "about": "Test - Edited",
            "website": "https://newtest.com"
        }
        response = self.client.post(reverse("streaming_platform-list"), data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_modify(self):
        """
        Test that admin users can modify streaming platform data.
        """
        self.client.login(username="admin_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "Test",
            "about": "Test - Edited",
            "website": "https://newtest.com"
        }
        
        response = self.client.post(reverse("streaming_platform-list"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
