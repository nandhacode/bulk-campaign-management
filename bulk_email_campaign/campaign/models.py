from django.db import models

class Recipient(models.Model):
    SUBSCRIBED = "Subscribed"
    UNSUBSCRIBED = "Unsubscribed"

    STATUS_CHOICES = [
        (SUBSCRIBED, "Subscribed"),
        (UNSUBSCRIBED, "Unsubscribed")
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscription_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
class Campaign(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_recipients = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.status})"
    
class DeliveryLog(models.Model):
    STATUS_SENT = "Sent"
    STATUS_FAILED = "Failed"
    STATUS_CHOICES = [
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="delivery_logs")
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    failure_reason = models.TextField(blank=True, default="")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["campaign", "recipient_email"]),
        ]

    def __str__(self):
        return f"{self.recipient_email} - {self.status}"