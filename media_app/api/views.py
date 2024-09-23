from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from media_app.api.pagination import *
from media_app.api.permissions import *
from media_app.api.serializers import *
from media_app.api.throttling import *
from media_app.models import *


class UserReviews(generics.ListAPIView):
    """
    List reviews filtered by a reviewer"s username.
    """

    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Retrieve reviews filtered by the "username" query parameter.
        """
        username = self.request.query_params.get("username", None)
        return Review.objects.filter(reviewer__username=username)

@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all available streaming platforms."
    ),
    retrieve=extend_schema(
        description="Retrieve a specific streaming platform by its ID."
    ),
    create=extend_schema(
        description="Create a new streaming platform. Only accessible to admin users."
    ),
    update=extend_schema(
        description="Update the details of an existing streaming platform by its ID."
    ),
    partial_update=extend_schema(
        description="Partially update specific fields of a streaming platform."
    ),
    destroy=extend_schema(
        description="Delete a specific streaming platform by its ID. Only accessible to admin users."
    ),
)
class StreamingPlatformViewSet(viewsets.ModelViewSet):
    """
    Performing CRUD operations on StreamingPlatform objects.
    """

    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

@extend_schema(
    parameters=[
        OpenApiParameter("username", description="Filter by reviewer username", required=False, type=str),
    ],
    responses=ReviewSerializer(many=True),
    description="List all reviews for a specific media, filtered by username or activity."
)
class ReviewList(generics.ListAPIView):
    """
    List all reviews for a specific media.
    Allows filtering by username and activity status.
    """

    pagination_class = ReviewPagination
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"reviewer__username", "active"}

    def get_queryset(self):
        """
        Retrieve reviews filtered by the media primary key (pk).
        """
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()
        
        pk = self.kwargs["pk"]
        return Review.objects.filter(media=pk).order_by("created")

@extend_schema_view(
    get=extend_schema(
        description="Retrieve a specific review by its ID."
    ),
    put=extend_schema(
        description="Update the details of an existing review by its ID."
    ),
    patch=extend_schema(
        description="Partially update specific fields of an existing review by its ID."
    ),
    delete=extend_schema(
        description="Delete a specific review by its ID. Only accessible to the review's owner or admin users."
    )
)
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a review.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_scope = "review-detail"

@extend_schema(
    description="Create a new review for a media."
)
class ReviewCreate(generics.CreateAPIView):
    """
    Create a new review for a media.
    Ensures that a user cannot review the same media multiple times.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def perform_create(self, serializer):
        """
        Custom behavior when creating a review, ensuring uniqueness and updating media ratings.
        """
        pk = self.kwargs.get("pk")
        media_object = Media.objects.get(pk=pk)
        reviewer = self.request.user

        review_queryset = Review.objects.filter(media=media_object, reviewer=reviewer)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this media.")

        new_avg_rating = serializer.validated_data["rating"]
        total_ratings = media_object.user_rating + 1
        media_object.avg_rating = ((media_object.avg_rating * media_object.user_rating) + new_avg_rating) / total_ratings

        media_object.user_rating = total_ratings
        media_object.save()

        serializer.save(media=media_object, reviewer=reviewer)

@extend_schema_view(
    get=extend_schema(
        responses={200: MediaSerializer(many=True)},
        description="Retrieve a list of all media objects."
    ),
    post=extend_schema(
        request=MediaSerializer,
        responses={201: MediaSerializer},
        description="Create a new media object. Only accessible to admin users."
    )
)
class MediaAPIView(APIView):
    """
    Listing and creating media objects.
    Creation is restricted to admin users.
    """

    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        """
        Retrieve and return all media objects.
        """
        media_objects = Media.objects.all()
        serializer = MediaSerializer(media_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new media object.
        """
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(
        responses={200: MediaSerializer},
        description="Retrieve a media object by its primary key (pk)."
    ),
    put=extend_schema(
        request=MediaSerializer,
        responses={200: MediaSerializer},
        description="Update an existing media object."
    ),
    delete=extend_schema(
        responses={204: None},
        description="Delete a media object."
    )
)
class MediaDetailAPIView(APIView):
    """
    Retrieving, updating, and deleting a single media object.
    """

    def get(self, request, pk):
        """
        Retrieve a media object by its primary key (pk).
        """
        try:
            media_object = Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            return Response({"Error": "Media not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MediaSerializer(media_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an existing media object.
        """
        media_object = Media.objects.get(pk=pk)
        serializer = MediaSerializer(media_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a media object.
        """
        media_object = Media.objects.get(pk=pk)
        media_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
