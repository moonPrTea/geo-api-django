from django.conf import settings
from django.contrib.gis.db import models
from .base import BaseModel
from .point import Point

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