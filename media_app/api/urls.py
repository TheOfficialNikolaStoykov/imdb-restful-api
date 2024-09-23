from django.urls import include, path
from rest_framework.routers import DefaultRouter

from media_app.api.views import *

router = DefaultRouter()
router.register("streaming_platform", StreamingPlatformViewSet, basename="streaming_platform")

urlpatterns = [
    path("", MediaAPIView.as_view(), name="media-list"),
    path("<int:pk>/", MediaDetailAPIView.as_view(), name="media-detail"),
    path("", include(router.urls)),
    path("<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),
    path("<int:pk>/review/create/", ReviewCreate.as_view(), name="review-create"),
    path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
    path("reviews/user/", UserReviews.as_view(), name="reviews-user"),
]