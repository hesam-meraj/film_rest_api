from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Subscription, Video, ShortHistory, Comment, Rating, Payment, SubscriptionType
from .serializers import (
    SubscriptionSerializer, 
    VideoSerializer, 
    ShortHistorySerializer, 
    CommentSerializer, 
    RatingSerializer, 
    PaymentSerializer,
    UserSerializer
)
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User = get_user_model()




class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def extend_subscription(self, request, pk=None):
        subscription = self.get_object()
        days = request.data.get('days', 0)
        try:
            subscription.extend_subscription(days)
            subscription.save()
            return Response({"status": "Subscription extended"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def cancel_subscription(self, request, pk=None):
        subscription = self.get_object()
        subscription.cancel_subscription()
        subscription.save()
        return Response({"status": "Subscription canceled"})

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        subscription_id = request.data.get('subscription')
        subscription = Subscription.objects.get(id=subscription_id)
        amount = subscription.subscription_type.price
        transaction_id = request.data.get('transaction_id')

        payment = Payment.objects.create(
            user=request.user,
            subscription=subscription,
            amount=amount,
            transaction_id=transaction_id
        )

        subscription.paid_amount = amount
        subscription.save()

        return Response({"status": "Payment successful", "transaction_id": transaction_id})

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class ShortHistoryViewSet(viewsets.ModelViewSet):
    queryset = ShortHistory.objects.all()
    serializer_class = ShortHistorySerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer