from django.shortcuts import redirect, render
from blogs.models import Blog, Category
from extraInfo.models import About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages

def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published')
    
    try:
        about = About.objects.get()
    except About.DoesNotExist: 
        about = None
        
    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()  
           
            auth.login(request, new_user)  
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user_obj = auth.authenticate(username=username, password=password)
            if user_obj is not None:
                auth.login(request, user_obj)
                messages.success(request, 'You have been logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')