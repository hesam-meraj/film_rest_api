from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Subscription, Film, Comment, Rating
from .serializers import UserSerializer, SubscriptionSerializer, FilmSerializer, CommentSerializer, RatingSerializer

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

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer