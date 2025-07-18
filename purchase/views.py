from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Inventory, RequestForMaterials, RequestForQuote, QuotationReceived, PurchasingOrder
from .forms import InventoryForm, RequestForm, RFQForm, QuotationForm, PurchaseOrderForm # type: ignore

# Create your views here.
@login_required
def inventory_list(request):
    items = Inventory.objects.all()
    return render(request, 'inventory/list.html', {'items': items})

@login_required
def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/add_item.html', {'form': form})

@login_required
def request_materials(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            material_request = form.save(commit=False)
            material_request.requester = request.user
            material_request.save()
            return redirect('material_requests')
    else:
        form = RequestForm()
    return render(request, 'materials/request_form.html', {'form': form})

@login_required
def material_requests(request):
    requests = RequestForMaterials.objects.all()
    return render(request, 'materials/request_list.html', {'requests': requests})

@login_required
def send_rfq(request, material_id):
    material = get_object_or_404(RequestForMaterials, pk=material_id)
    if request.method == 'POST':
        form = RFQForm(request.POST)
        if form.is_valid():
            rfq = form.save(commit=False)
            rfq.material_request = material
            rfq.save()
            return redirect('rfq_list')
    else:
        form = RFQForm()
    return render(request, 'rfq/send.html', {'form': form, 'material': material})

@login_required
def rfq_list(request):
    rfq = RequestForQuote.objects.all()
    return render(request, 'rfq/list.html', {'rfq': rfq})


