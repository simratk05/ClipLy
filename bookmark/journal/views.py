from django.shortcuts import render,redirect, get_object_or_404
from .forms import CreateUserForm,LoginForm,BookmarkForm,UpdateUserForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.contrib import messages
from .models import Bookmark
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.response import Response
from .serializers import BookmarkSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json
from .models import User
from django.contrib.auth.decorators import user_passes_test
from .forms import LoginForm
from rest_framework.permissions import AllowAny



def homepage(request):
    return render(request,'journal/index.html')
def register(request):
     form=CreateUserForm()
     if request.method=="POST":
          form=CreateUserForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request,"USER CREATED.")
               return redirect('my-login')
     context={'RegistrationForm':form}
     return render(request,'journal/register.html',context)




def my_login(request):
     form=LoginForm()
     if request.method=='POST':
          form=LoginForm(request,data=request.POST)
          if form.is_valid():
               username=request.POST.get('username')
               password=request.POST.get('password')

               user=authenticate(request,username=username,password=password)
               if user is not None:
                    auth.login(request,user)

                    return redirect('dashboard')
     context={'LoginForm': form}
     return render(request,'journal/my-login.html',context)
def user_logout(request):
     auth.logout(request)
     return redirect("")



@login_required(login_url='my-login')
def dashboard(request):
     return render(request,'journal/dashboard.html')

@login_required
def add_bookmark(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
            return redirect('my_bookmarks')  # Redirect to a success page or bookmarks list
        else:
            context = {'form': form, 'error_message': 'Invalid data. Please provide both URL and Title.'}
            return render(request, 'journal/add-bookmark.html', context)
    else:
        form = BookmarkForm()
        return render(request, 'journal/add-bookmark.html', {'form': form})


@login_required(login_url='my-login')
def my_bookmarks(request):
    bookmarks = Bookmark.objects.all()
    context = {'allbookmarks': bookmarks}
    return render(request, 'journal/my-bookmarks.html', context)

@login_required
def update_bookmarks(request, pk):
    # Use get_object_or_404 to handle the case where the Bookmark does not exist
    bookmark = get_object_or_404(Bookmark, id=pk)
    form = BookmarkForm(instance=bookmark)
    
    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return redirect('my_bookmarks')  # Ensure 'my_bookmarks' is defined in your URLconf
    
    context = {'updatebookmark': form}
    return render(request, 'journal/update-bookmarks.html', context)

@login_required(login_url='my-login')
def delete_bookmark(request, pk):
    # Get the bookmark or return a 404 error if not found
    bookmark = get_object_or_404(Bookmark, id=pk)

    if request.method == 'POST':
        bookmark.delete()
        return redirect('my_bookmarks')  # Ensure 'my_bookmarks' is correctly defined in your URLconf

    # If the method is not POST, render the delete confirmation template
    return render(request, 'journal/delete-bookmark.html', {'bookmark': bookmark})

@csrf_exempt
@api_view(['POST'])
def save_bookmark(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            title = data.get('title')

            bookmark = Bookmark(url=url, title=title)
            bookmark.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': str(e)})
    return JsonResponse({'status': 'error', 'errors': 'Invalid request method'})


@login_required(login_url='my-login')
def profile(request):
    form=UpdateUserForm(instance=request.user)
    if request.method=='POST':
        form=UpdateUserForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'ProfileForm':form}
    return render(request, 'journal/profile.html',context)

@login_required(login_url='my-login')
def delete_account(request):
     if request.method=='POST':
         deleteUser=User.objects.get(username=request.user)
         deleteUser.delete()
         return redirect("")
     return render(request, 'journal/delete-account.html')







