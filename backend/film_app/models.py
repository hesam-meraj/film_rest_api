from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_data = models.DateTimeField(auto_now_add=True)
    # file = models.FileField(upload_to='films/')
    views = models.PositiveBigIntegerField(default=0)
    def __str__(self):
        return self.title
    
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    def extend_subscription(self, days):
        if self.is_active:
            self.end_date += timedelta(days=days)
        else:
            raise ValueError("Subscription is not active")

    def cancel_subscription(self):
        self.is_active = False
        self.end_date = timezone.now()

    def __str__(self):
        return f"{self.user.username}'s subscription"

    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating between 1 to 5
    rated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Rating {self.score} by {self.user.username} on {self.video.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Film, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"



