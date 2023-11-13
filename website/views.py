from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages       
from .forms import SignUpForm, AddRecordForm, PhotoForm
from .models import Record, Photo
from .tasks import send_delayed_emails
from django.utils import timezone


# Create your views here.
def home(request):
    records = Record.objects.all()
    #login logic
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In...")
            return redirect('home')
        else:
            messages.success(request, 'There was an erroe logging in please try again...')
            return redirect('home') 
    else:
        return render(request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You Have Succesfully Registered. Welcome Aboard')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'You Must Be Logged In to View That Page')
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record Deleted SUccesfully...')
        return redirect('home')
    else:
        messages.success(request, 'You Must Be Logged In to Do That')
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, 'You Must Be Logged To Add a Record')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Has Been Updated')
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, 'You Must Be Logged To Add a Record')
        return redirect('home')   
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo_detail.html', {'photo': photo})

def photo_create(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'photo_form.html', {'form': form})

def photo_update(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'photo_form.html', {'form': form})

def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        photo.delete()
        return redirect('photo_list')
    return render(request, 'photo_confirm_delete.html', {'photo': photo})

def photo_view(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo_view.html', {'photo': photo})

def send_all_emails(request):
    # Schedule the task to send emails to all records in the future (e.g., 1 hour later)
    send_delayed_emails.apply_async(
        ('Subject', 'Message'),
        eta=timezone.now() + timezone.timedelta(hours=1)
    )
    return redirect('success')  # Redirect to a success page

def send_email_to_all(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Schedule the task to send emails to all records in the future (e.g., 1 hour later)
        for record in Record.objects.all():
            send_delayed_emails.apply_async(
                (subject, message),
                eta=timezone.now() + timezone.timedelta(hours=1)
            )

        return redirect('success')  # Redirect to a success page

    return render(request, 'send_email_to_all.html')
