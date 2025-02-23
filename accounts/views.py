from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact
from cars.models import Car
from django.core.mail import send_mail

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')
def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in.')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request, 'You are registered successfully.')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
def dashboard(request):
    user_inquiry=Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data={
        'inquiries':user_inquiry,
    }
    return render(request,'accounts/dashboard.html',data)
def logout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request,'you are successfully logged out')
        return redirect('home')
    return redirect('home')


def requests(request):
    Requests = Contact.objects.all().order_by("-id")
    if request.method == "POST":
        ContactId = request.POST['Contact']
        contactDetails = Contact.objects.get(id=ContactId)
        carDetails = Car.objects.get(id=contactDetails.car_id)
        print(contactDetails.email)

        subject='Car Details',

        try:
            send_mail(
                subject,
                'You have a new inquiry for the car ' + carDetails.car_title + '. Please login to your admin panel for more info.',
                'carportal8@gmail.com',
                [contactDetails.email],
                fail_silently=False,
            )
            messages.success(request, "Mail sent")
        except:
            messages.error(request, "failed to send")
        return redirect("requests")
        
    return render(request, "accounts/requests.html", {"Requests":Requests})