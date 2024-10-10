from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=False)


class SubscriptionType(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    duration_days = models.IntegerField()  

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_videos')
    file = models.FileField(upload_to='videos/')
    is_public = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey("Subscription", on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.subscription}"
    
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    paid_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def extend_subscription(self, days):
        if self.is_active:
            self.end_date += timedelta(days=days)
        else:
            raise ValueError("Subscription is not active")

    def cancel_subscription(self):
        self.is_active = False
        self.end_date = timezone.now()

    def __str__(self):
        return f"{self.user.username}'s {self.subscription_type.name} subscription"

class ShortHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    last_watched = models.DateTimeField(auto_now=True)
    watch_duration = models.DurationField()

    def __str__(self):
        return f"{self.user.username} watched {self.video.title}"

    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 10)]) # like imdb  
    rated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.score} by {self.user.username} on {self.video.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"



