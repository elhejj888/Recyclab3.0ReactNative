from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from authentication.models import User

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})

def subscribe(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        is_admin = request.POST.get('is_admin', False)

        # Create a new user object
        user = User.objects.create_user(username=username, password=password)
        user.phone = phone
        user.address = address
        user.is_admin = is_admin
        user.save()

        return JsonResponse({'success': True, 'message': 'Account created successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Account creation failed'})
