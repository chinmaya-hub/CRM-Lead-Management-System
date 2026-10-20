from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q

from .models import Lead, Activity, FollowUp, Customer
from .forms import LeadForm, ActivityForm, FollowUpForm


# =========================
# DASHBOARD
# =========================
def dashboard(request):
    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status='New').count()
    qualified_leads = Lead.objects.filter(status='Qualified').count()
    closed_leads = Lead.objects.filter(status='Closed').count()
    total_customers = Customer.objects.count()

    recent_leads = Lead.objects.order_by('-created_at')[:5]

    # Lead status chart data
    status_data = (
        Lead.objects.values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )

    # Lead source chart data
    source_data = (
        Lead.objects.values('source')
        .annotate(total=Count('id'))
        .order_by('source')
    )

    # Lead pipeline data in the required order
    pipeline_statuses = [
        'New',
        'Contacted',
        'Qualified',
        'Proposal',
        'Closed',
    ]

    pipeline_data = [
        Lead.objects.filter(status=status).count()
        for status in pipeline_statuses
    ]

    context = {
        'total_leads': total_leads,
        'new_leads': new_leads,
        'qualified_leads': qualified_leads,
        'closed_leads': closed_leads,
        'total_customers': total_customers,
        'recent_leads': recent_leads,
        'status_data': list(status_data),
        'source_data': list(source_data),
        'pipeline_statuses': pipeline_statuses,
        'pipeline_data': pipeline_data,
    }

    return render(request, 'leads/dashboard.html', context)


# =========================
# ADD LEAD
# =========================
def add_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = LeadForm()

    return render(request, 'leads/add_lead.html', {'form': form})


# =========================
# LEAD LIST, SEARCH AND FILTER
# =========================
def lead_list(request):
    leads = Lead.objects.all().order_by('-created_at')

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '')
    source = request.GET.get('source', '')

    if search:
        leads = leads.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(company__icontains=search)
            | Q(phone__icontains=search)
        )

    if status:
        leads = leads.filter(status=status)

    if source:
        leads = leads.filter(source=source)

    context = {
        'leads': leads,
        'search': search,
        'selected_status': status,
        'selected_source': source,
        'status_choices': Lead.STATUS_CHOICES,
        'source_choices': Lead.SOURCE_CHOICES,
    }

    return render(request, 'leads/lead_list.html', context)


# =========================
# EDIT LEAD
# =========================
def edit_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead)

    return render(
        request,
        'leads/edit_lead.html',
        {
            'form': form,
            'lead': lead,
        }
    )


# =========================
# DELETE LEAD
# =========================
def delete_lead(request, lead_id):
    if request.method != 'POST':
        return redirect('lead_list')

    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()

    return redirect('lead_list')


# =========================
# ACTIVITY LOGS
# =========================
def lead_activities(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == 'POST':
        form = ActivityForm(request.POST)

        if form.is_valid():
            activity = form.save(commit=False)
            activity.lead = lead
            activity.save()

            return redirect('lead_activities', lead_id=lead.id)
    else:
        form = ActivityForm()

    activities = lead.activities.order_by('-created_at')

    context = {
        'lead': lead,
        'form': form,
        'activities': activities,
    }

    return render(request, 'leads/activities.html', context)


# =========================
# FOLLOW-UP MANAGEMENT
# =========================
def lead_followups(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == 'POST':
        form = FollowUpForm(request.POST)

        if form.is_valid():
            followup = form.save(commit=False)
            followup.lead = lead
            followup.save()

            return redirect('lead_followups', lead_id=lead.id)
    else:
        form = FollowUpForm()

    followups = lead.followups.order_by('completed', 'scheduled_at')

    context = {
        'lead': lead,
        'form': form,
        'followups': followups,
    }

    return render(request, 'leads/followups.html', context)


# =========================
# CONVERT LEAD TO CUSTOMER
# =========================
def convert_lead(request, lead_id):
    if request.method != 'POST':
        return redirect('lead_list')

    lead = get_object_or_404(Lead, id=lead_id)

    if not Customer.objects.filter(lead=lead).exists():
        Customer.objects.create(lead=lead)
        lead.status = 'Closed'
        lead.save()

    return redirect('lead_list')