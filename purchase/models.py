from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('escalated', 'escalated'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    cost_estimate = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} by {self.user.username}"
    
    class Approval(models.Model):
        purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
        approver = models.ForeignKey(User, on_delete=models.CASCADE)
        action = models.CharField(max_length=20, choices=[
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('escalated', 'Escalated'),
            ])
        comments = models.TextField(blank=True)
        approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.approver.username} on {self.purchase_request}" 
