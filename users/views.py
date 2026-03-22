from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from users.forms import RegistrationForm
from marketplace.models import Trade

# Create your views here.
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    return render(request, 'registration/register.html', {'form': form})

@login_required
def trades(request):
    # Trades sent by the user (pending or rejected/too low)
    trades_sent = Trade.objects.filter(
        proposer=request.user
    ).exclude(status='A').select_related(
        'target_offering__hobby', 'target_offering__owner', 
        'offered_offering__hobby', 'offered_offering__owner'
    ).order_by('-created_at')
    
    # Trades received by the user (pending or rejected/too low)
    trades_received = Trade.objects.filter(
        target_offering__owner=request.user
    ).exclude(status='A').select_related(
        'target_offering__hobby', 'target_offering__owner', 
        'offered_offering__hobby', 'offered_offering__owner', 'proposer'
    ).order_by('-created_at')
    
    # Completed trades (accepted)
    trades_completed = Trade.objects.filter(
        status='A'
    ).filter(
        models.Q(proposer=request.user) | models.Q(target_offering__owner=request.user)
    ).select_related(
        'target_offering__hobby', 'target_offering__owner', 
        'offered_offering__hobby', 'offered_offering__owner', 'proposer'
    ).order_by('-updated_at')
    
    return render(request, 'profile/trades.html', {
        'trades_sent': trades_sent,
        'trades_received': trades_received,
        'trades_completed': trades_completed,
    })