from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count, Avg
from django.http import HttpResponse
from django.utils import timezone
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import User, Complaint, ComplaintRemark, ComplaintRating
from .forms import ComplaintForm, RatingForm



def homepage(request):
    """Public landing page - redirects logged-in users to dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Live stats for the homepage
    stats = {
        'total_resolved': Complaint.objects.filter(status='RESOLVED').count(),
        'total_users': User.objects.filter(role='USER').count(),
        'avg_rating': ComplaintRating.objects.aggregate(avg=Avg('stars'))['avg'],
        'total_complaints': Complaint.objects.count(),
    }
    if stats['avg_rating']:
        stats['avg_rating'] = round(stats['avg_rating'], 1)
    
    return render(request, 'homepage.html', {'stats': stats})


@login_required
def dashboard(request):
    if request.user.role == 'ADMIN':
        complaints = Complaint.objects.all()
    elif request.user.role == 'MANAGER':
        complaints = Complaint.objects.filter(assigned_to=request.user)
    else:
        complaints = Complaint.objects.filter(created_by=request.user)

    overdue_count = sum(1 for c in complaints if c.is_overdue)
        
    stats = {
        'total': complaints.count(),
        'open': complaints.filter(status='OPEN').count(),
        'progress': complaints.filter(status='IN_PROGRESS').count(),
        'resolved': complaints.filter(status='RESOLVED').count(),
        'overdue': overdue_count,
    }
    recent_complaints = complaints.order_by('-created_at')[:5]
    
    chart_data = None
    if request.user.role == 'ADMIN':
        category_counts = Complaint.objects.values('category').annotate(count=Count('id'))
        status_counts = Complaint.objects.values('status').annotate(count=Count('id'))
        avg_rating = ComplaintRating.objects.aggregate(avg=Avg('stars'))['avg']
        
        chart_data = {
            'categories': list(category_counts),
            'statuses': list(status_counts),
            'avg_rating': round(avg_rating, 1) if avg_rating else None,
            'total_ratings': ComplaintRating.objects.count(),
        }
    
    return render(request, 'complaints/dashboard.html', {
        'stats': stats, 
        'recent_complaints': recent_complaints,
        'chart_data': chart_data,
        'overdue_count': overdue_count,
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

    overdue_count = sum(1 for c in complaints if c.is_overdue)
        
    return render(request, 'complaints/complaint_list.html', {
        'complaints': complaints,
        'current_status': status_filter,
        'overdue_count': overdue_count,
    })

@login_required
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    
    # Get overdue count for notification bell
    if request.user.role == 'ADMIN':
        all_complaints = Complaint.objects.all()
    elif request.user.role == 'MANAGER':
        all_complaints = Complaint.objects.filter(assigned_to=request.user)
    else:
        all_complaints = Complaint.objects.filter(created_by=request.user)
    overdue_count = sum(1 for c in all_complaints if c.is_overdue)
    
    return render(request, 'complaints/complaint_form.html', {'form': form, 'overdue_count': overdue_count})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if not (complaint.created_by == request.user or complaint.assigned_to == request.user or request.user.role == 'ADMIN'):
        return redirect('dashboard')
        
    managers = User.objects.filter(role='MANAGER') if request.user.role == 'ADMIN' else None
    rating_form = None
    existing_rating = None

    try:
        existing_rating = complaint.rating
    except ComplaintRating.DoesNotExist:
        pass

    # Show rating form only if complaint is resolved and rated by the complaint creator
    if complaint.status == 'RESOLVED' and complaint.created_by == request.user and not existing_rating:
        rating_form = RatingForm()
        
    if request.method == 'POST':
        action = request.POST.get('action', 'update')

        # Handle re-open action
        if action == 'reopen' and complaint.status == 'RESOLVED' and complaint.created_by == request.user:
            complaint.status = 'OPEN'
            complaint.reopen_count += 1
            complaint.save()
            ComplaintRemark.objects.create(
                complaint=complaint,
                remark=f'Complaint re-opened by {request.user.username} (Reopen #{complaint.reopen_count}). Issue not resolved satisfactorily.',
                added_by=request.user,
                status_at_remark='OPEN'
            )
            return redirect('complaint_detail', pk=pk)

        # Handle star rating submission
        elif action == 'rate' and complaint.status == 'RESOLVED' and complaint.created_by == request.user and not existing_rating:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.complaint = complaint
                rating.rated_by = request.user
                rating.save()
                return redirect('complaint_detail', pk=pk)

        # Handle status/remark update (for managers/admins)
        elif request.user.role in ['ADMIN', 'MANAGER']:
            remark_text = request.POST.get('remark')
            new_status = request.POST.get('status')
            
            if request.user.role == 'ADMIN':
                assigned_to_id = request.POST.get('assigned_to')
                if assigned_to_id:
                    manager = get_object_or_404(User, id=assigned_to_id)
                    complaint.assigned_to = manager
                    complaint.save()
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
                    send_mail(
                        f'Update on your complaint: {complaint.title}',
                        f'Hello {complaint.created_by.username},\nYour complaint "{complaint.title}" has been updated to {complaint.get_status_display()}.\n\nRemark: {remark_text}\n\nTrack progress: {request.build_absolute_uri()}',
                        'noreply@cmspro.com',
                        [complaint.created_by.email],
                        fail_silently=True,
                    )
            return redirect('complaint_detail', pk=pk)

    # Get overdue count for notification bell
    if request.user.role == 'ADMIN':
        all_complaints = Complaint.objects.all()
    elif request.user.role == 'MANAGER':
        all_complaints = Complaint.objects.filter(assigned_to=request.user)
    else:
        all_complaints = Complaint.objects.filter(created_by=request.user)
    overdue_count = sum(1 for c in all_complaints if c.is_overdue)

    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'managers': managers,
        'rating_form': rating_form,
        'existing_rating': existing_rating,
        'overdue_count': overdue_count,
    })

@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('homepage')


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

@login_required
def export_complaints_csv(request):
    """Admin-only: Export all complaints to CSV"""
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="complaints_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ref ID', 'Title', 'Category', 'Status', 'Raised By', 'Assigned To', 'Created At', 'Days Open', 'Overdue', 'Reopen Count', 'Rating'])

    complaints = Complaint.objects.select_related('created_by', 'assigned_to').prefetch_related('rating').all().order_by('-created_at')
    for c in complaints:
        try:
            rating = c.rating.stars
        except Exception:
            rating = 'N/A'
        writer.writerow([
            f'REF-{c.id:05d}',
            c.title,
            c.get_category_display(),
            c.get_status_display(),
            c.created_by.username,
            c.assigned_to.username if c.assigned_to else 'Unassigned',
            c.created_at.strftime('%Y-%m-%d %H:%M'),
            c.days_open,
            'Yes' if c.is_overdue else 'No',
            c.reopen_count,
            rating,
        ])
    return response

@login_required
def export_complaints_pdf(request):
    """Admin-only: Export all complaints to a professional PDF report"""
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="complaints_report_{timezone.now().strftime("%Y%m%d_%H%M")}.pdf"'

    # Create a buffer for the PDF
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#6366f1"),
        alignment=1,
        spaceAfter=30
    )

    # Title
    elements.append(Paragraph("CMS PRO — Enterprise Complaint Report", title_style))
    elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Data for the table
    data = [['Ref ID', 'Title', 'Category', 'Status', 'Raised By', 'Assigned To', 'Created At', 'Rating']]
    
    complaints = Complaint.objects.select_related('created_by', 'assigned_to').prefetch_related('rating').all().order_by('-created_at')
    
    for c in complaints:
        try:
            rating = f"{c.rating.stars}★"
        except Exception:
            rating = 'N/A'
            
        data.append([
            f'REF-{c.id:05d}',
            Paragraph(c.title[:30], styles['Normal']),
            c.get_category_display(),
            c.get_status_display(),
            c.created_by.username,
            c.assigned_to.username if c.assigned_to else 'Unassigned',
            c.created_at.strftime('%Y-%m-%d'),
            rating
        ])

    # Create table
    table = Table(data, colWidths=[60, 150, 80, 70, 70, 70, 70, 50])
    
    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    table.setStyle(style)
    
    elements.append(table)

    # Build PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
