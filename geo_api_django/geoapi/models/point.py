from django.contrib.gis.db import models
from django.conf import settings

from .base import BaseModel


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