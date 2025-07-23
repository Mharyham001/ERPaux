from django import forms
from .models import RequestForMaterials, RequestForQuote, QuotationReceived, PurchasingOrder
from .models import RequestForQuote


class MaterialRequestForm(forms.ModelForm):
    class Meta:
        model = RequestForMaterials
        fields = ['item', 'quantity_requested', 'purpose']

class MaterialApprovalForm(forms.ModelForm):
    class Meta:
        model = RequestForMaterials
        fields = ['status']

class RFQForm(forms.ModelForm):
    class Meta:
        model = RequestForQuote
        fields = ['supplier_name', 'contact_email']

