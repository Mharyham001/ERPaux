from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RequestForMaterials
from .forms import MaterialRequestForm, MaterialApprovalForm
from .models import RequestForQuote
from .forms import RFQForm

# Submit request (staff)
@login_required
def submit_request(request):
    if request.method == 'POST':
        form = MaterialRequestForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.requester = request.user
            material.save()
            return redirect('my_requests')
    else:
        form = MaterialRequestForm()
    return render(request, 'materials/submit.html', {'form': form})

# View all requests (for managers)
@login_required
def view_requests(request):
    if request.user.groups.filter(name__in=['Manager', 'Finance']).exists():
        requests = RequestForMaterials.objects.all()
    else:
        requests = RequestForMaterials.objects.filter(requester=request.user)
    return render(request, 'materials/list.html', {'requests': requests})

# Approve or reject (manager/finance)
@login_required
def approve_request(request, request_id):
    req = get_object_or_404(RequestForMaterials, id=request_id)
    if request.method == 'POST':
        form = MaterialApprovalForm(request.POST, instance=req)
        if form.is_valid():
            approval = form.save(commit=False)
            approval.approved_by = request.user
            approval.save()
            return redirect('view_requests')
    else:
        form = MaterialApprovalForm(instance=req)
    return render(request, 'materials/approve.html', {'form': form, 'req': req})


# Send RFQ for an approved material request
@login_required
def send_rfq(request, material_id):
    material = get_object_or_404(RequestForMaterials, id=material_id, status='Approved')

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

# View all RFQs
@login_required
def rfq_list(request):
    rfqs = RequestForQuote.objects.all()
    return render(request, 'rfq/list.html', {'rfqs': rfqs})
