from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    SubscriptionViewSet, 
    VideoViewSet, 
    ShortHistoryViewSet, 
    CommentViewSet, 
    RatingViewSet, 
    UserRegisterView,
    UserLoginView,
    LogoutView
)

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'history', ShortHistoryViewSet, basename='history')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),

    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('subscriptions/<int:pk>/extend/', SubscriptionViewSet.as_view({'post': 'extend_subscription'})),
    path('subscriptions/<int:pk>/cancel/', SubscriptionViewSet.as_view({'post': 'cancel_subscription'})),
]
