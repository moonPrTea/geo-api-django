from django.contrib.gis.db import models
from django.conf import settings
from django.utils import timezone


# base model with common fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Point(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="description to specify current point"
    )
    location = models.PointField(geography=True) # with latitude and longitude
    
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='points'
    )
    
    class Meta:
        db_table = "point"
        db_table_comment = "points information"
        ordering = ['title']
    
    @property
    def latitude(self):
        return self.location.y if self.location else None
    
    @property
    def longitude(self):
        return self.location.x if self.location else None
    
    def __str__(self):
        return {self.title}


class Message(BaseModel):
    point = models.ForeignKey(
        Point, 
        on_delete=models.CASCADE,
    )
    
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    message_text = models.TextField(
        blank=True, 
        null=True,
        help_text="all messages from users"
    )
    
    class Meta:
        db_table = "message"
        db_table_comment = "messages for points"
        ordering = ['created_at']
    
    def __str__(self):
        return f"message by {self.creator} at {self.created_at}"