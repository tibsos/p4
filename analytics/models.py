from django.db import models as m

from uuid import uuid4 as u4

from django.db import models
import uuid

class Visit(models.Model):
    ip = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)  # Добавляем обратно city
    entered_at = models.DateTimeField()
    left_at = models.DateTimeField(null=True, blank=True)
    url = models.URLField(null=True)
    mobile = models.BooleanField(default=False)
    uid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.ip} - {self.entered_at}"
    
    class Meta:
        verbose_name = "Visit"
        verbose_name_plural = "Visits"


    
class Event(models.Model):
    session_id = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50)
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.session_id} - {self.event_type} at {self.timestamp}"
