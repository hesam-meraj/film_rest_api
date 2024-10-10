from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, FilmViewSet,  CommentViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'videos', FilmViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/<int:pk>/extend/', SubscriptionViewSet.as_view({'post': 'extend_subscription'})),
    path('subscriptions/<int:pk>/cancel/', SubscriptionViewSet.as_view({'post': 'cancel_subscription'})),
]