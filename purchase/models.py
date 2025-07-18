from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Inventory(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.CharField(max_length=50)  
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

class RequestForMaterials(models.Model):
    requester_name = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    item_id = models.ForeignKey(Inventory, on_delete=models.CASCADE) # type: ignore
    quantity_requested = models.PositiveIntegerField()
    purpose = models.TextField()
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')

    def __str__(self):
        return f"Request by {self.requester.username} for {self.item}"

class RequestForQuote(models.Model):
    material_request = models.ForeignKey(RequestForMaterials, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    rfq_date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('Sent', 'Sent'),
        ('Pending', 'Pending'),
        ('Responded', 'Responded'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Sent')

    def __str__(self):
        return f"RFQ to {self.vendor_name}"
    
class QuotationReceived(models.Model):
    rfq_id = models.ForeignKey(RequestForQuote, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255)
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_time = models.CharField(max_length=100)
    quotation_date = models.DateTimeField(auto_now_add=True)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"Quote from {self.vendor_name} for RFQ #{self.rfq.id}"

class PurchasingOrder(models.Model):
    po_id = models.CharField(max_length=100, unique=True)
    quotation_id = models.ForeignKey(QuotationReceived, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivery_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"PO #{self.po_number}"

