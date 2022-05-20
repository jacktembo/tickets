from django.db import models


class KazangSession(models.Model):
    """
    Kazang (Content Ready Session).
    """
    session_uuid = models.CharField(max_length=255, editable=False)
    date_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_uuid


