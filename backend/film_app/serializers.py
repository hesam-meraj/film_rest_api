from rest_framework import serializers
from .models import (
    User, Subscription, SubscriptionType, Video, ShortHistory, Comment, Rating, Payment
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = ['name', 'price', 'duration_days']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['user', 'subscription', 'amount', 'payment_date', 'transaction_id']

class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_type = SubscriptionTypeSerializer()

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'subscription_type', 'start_date', 'end_date', 'is_active', 'paid_amount']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'upload_date', 'uploader', 'file', 'is_public']

class ShortHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortHistory
        fields = ['id', 'user', 'video', 'last_watched', 'watch_duration']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'video', 'text', 'created_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'video', 'score', 'rated_at']
