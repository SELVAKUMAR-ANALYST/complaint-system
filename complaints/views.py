from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import User, Complaint, ComplaintRemark
from .forms import ComplaintForm

@login_required
def dashboard(request):
    if request.user.role == 'ADMIN':
        complaints = Complaint.objects.all()
    elif request.user.role == 'MANAGER':
        complaints = Complaint.objects.filter(assigned_to=request.user)
    else:
        complaints = Complaint.objects.filter(created_by=request.user)
        
    stats = {
        'total': complaints.count(),
        'open': complaints.filter(status='OPEN').count(),
        'progress': complaints.filter(status='IN_PROGRESS').count(),
        'resolved': complaints.filter(status='RESOLVED').count(),
    }
    recent_complaints = complaints.order_by('-created_at')[:5]
    
    chart_data = None
    if request.user.role == 'ADMIN':
        from django.db.models import Count
        category_counts = Complaint.objects.values('category').annotate(count=Count('id'))
        status_counts = Complaint.objects.values('status').annotate(count=Count('id'))
        
        chart_data = {
            'categories': list(category_counts),
            'statuses': list(status_counts),
        }
    
    return render(request, 'complaints/dashboard.html', {
        'stats': stats, 
        'recent_complaints': recent_complaints,
        'chart_data': chart_data
    })

@login_required
def complaint_list(request):
    status_filter = request.GET.get('status', 'ALL')
    
    if request.user.role == 'ADMIN':
        complaints = Complaint.objects.all()
    elif request.user.role == 'MANAGER':
        complaints = Complaint.objects.filter(assigned_to=request.user)
    else:
        complaints = Complaint.objects.filter(created_by=request.user)
    
    if status_filter != 'ALL':
        complaints = complaints.filter(status=status_filter)
        
    return render(request, 'complaints/complaint_list.html', {
        'complaints': complaints,
        'current_status': status_filter
    })

@login_required
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/complaint_form.html', {'form': form})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    # Ensure user can only see their own complaint or if it's assigned to them (for managers) or if they are admin
    if not (complaint.created_by == request.user or complaint.assigned_to == request.user or request.user.role == 'ADMIN'):
        return redirect('dashboard')
        
    managers = User.objects.filter(role='MANAGER') if request.user.role == 'ADMIN' else None
        
    if request.method == 'POST':
        # Handle status/remark update (for managers/admins)
        if request.user.role in ['ADMIN', 'MANAGER']:
            remark_text = request.POST.get('remark')
            new_status = request.POST.get('status')
            
            # Handle assignment (for admins)
            if request.user.role == 'ADMIN':
                assigned_to_id = request.POST.get('assigned_to')
                if assigned_to_id:
                    manager = get_object_or_404(User, id=assigned_to_id)
                    complaint.assigned_to = manager
                    complaint.save()
                    
                    # Notify Manager
                    send_mail(
                        f'New Complaint Assigned: {complaint.title}',
                        f'Hello {manager.username}, a new complaint has been assigned to you.\n\nTitle: {complaint.title}\nCategory: {complaint.get_category_display()}\n\nCheck details here: {request.build_absolute_uri()}',
                        'noreply@cmspro.com',
                        [manager.email],
                        fail_silently=True,
                    )

            if remark_text:
                ComplaintRemark.objects.create(
                    complaint=complaint,
                    remark=remark_text,
                    added_by=request.user,
                    status_at_remark=new_status
                )
                if new_status:
                    complaint.status = new_status
                    complaint.save()
                    
                    # Notify User
                    send_mail(
                        f'Update on your complaint: {complaint.title}',
                        f'Hello {complaint.created_by.username},\nYour complaint "{complaint.title}" has been updated to {complaint.get_status_display()}.\n\nRemark: {remark_text}\n\nTrack progress: {request.build_absolute_uri()}',
                        'noreply@cmspro.com',
                        [complaint.created_by.email],
                        fail_silently=True,
                    )
            return redirect('complaint_detail', pk=pk)

    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'managers': managers
    })

@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('login')

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken. Please choose another one.')
            return render(request, 'registration/register.html')
            
        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/register.html')
