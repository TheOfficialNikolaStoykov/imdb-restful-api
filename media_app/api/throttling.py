from rest_framework.throttling import UserRateThrottle


class ReviewCreateThrottle(UserRateThrottle):
    """
    Throttle class for limiting the rate of review creation by users.
    """

    scope = "review-create"


class ReviewListThrottle(UserRateThrottle):
    """
    Throttle class for limiting the rate of requests to list reviews.
    """

    scope = "review-list"
