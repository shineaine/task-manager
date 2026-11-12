from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    
    # 1. Automatic diary timestamp (Records exact moment created)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 2. Manual target timestamp (Selected date/time to be done)
    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title