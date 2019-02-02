from django.db import models
from nomadgram.users import models as user_models
from nomadgram.images import models as image_models

class Notification(image_models.TimeStampedModel):

    TYPE_CHOICE = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name='creator')
    to = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name='to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICE)
    image = models.ForeignKey(image_models.Image, on_delete=models.PROTECT, null=True, blank=True)