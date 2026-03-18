#from django.db import models
from django.db import models

class ProjectAbstract(models.Model):
    # We save the text and the exact time it was submitted
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project ID: {self.id} - {self.content[:50]}..."
