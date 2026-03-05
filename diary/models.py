from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 嬉しい'),
        ('normal', '😐 普通'),
        ('sad', '😢 悲しい'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='normal')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date}|{self.title}"
    
    class Meta:
        ordering = ['-date']