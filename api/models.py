from django.db import models
from django.utils import timezone

class UserQuery(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now, editable=False)
    user_query = models.TextField(default="")
    ai_answer = models.TextField(default="")

    def __str__(self):
        return f"{self.id}: {self.date}: {self.user_query[:50]}..."

    class Meta:
        verbose_name = "User Query"
        verbose_name_plural = "User Queries"
