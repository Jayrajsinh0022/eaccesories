from django.shortcuts import render, redirect
from user_app.models import Contact_us
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from store_app.models import Order, Product, Categories, Filter_Price, Color, Brand, Tag, Order, OrderItem


def Contact_Page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_from, [
                      'jayrajsisodiya964@gmail.com'])
            contact.save()
            return redirect('')
        except:
            return redirect('contact')

    return render(request, 'user_app/contact.html')


# def HandleRegister(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('pass1')
#         pass2 = request.POST.get('pass2')

#         customer = User.objects.create_user(username,email,pass1)
#         customer.first_name = first_name
#         customer.last_name = last_name
#         customer.save()
#         return redirect('register')
#     return render(request,'user_app/auth.html')



def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == pass2:
             if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Exists!")
                return redirect('register')
             else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email Already Exists!")
                    return redirect('register')
                else:
                   customer = User.objects.create_user(username, email, pass1)
                   customer.first_name = first_name
                   customer.last_name = last_name
                   customer.save()

                   # Send welcome email to new user
                   subject = "Welcome to our website"
                   message = f"Dear {first_name},\n\nThank you for registering on our website!"
                   from_email = settings.EMAIL_HOST_USER
                   recipient_list = [email]
                   send_mail(subject, message, from_email, recipient_list)

                   # Redirect user to login page
                   messages.success(request, "Registration successful. Please log in.")
                   return redirect('login')
        else:
            messages.info(request, "Password and Confirm password Mismatch!")
            return redirect('register')              

    return render(request, 'user_app/auth.html')

    


def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('')
        else:
            return redirect('login')
        messages.info(request,"Login Failed Please Try Again")
    return render(request,'user_app/auth.html')



# def HandleLogin(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username = username, password = password)
#         if user is not None:
#             login(request,user)
#             return redirect('')
#         else:
#             return redirect('login')

#return render(request,'user_app/auth.html')

def HandleLogout(request):
    logout(request)
    redirect('')
    return render(request,'user_app/auth.html')

def Account(request):

   return render(request,'user_app/account.html')

    
def PROFILE(request):
   
    return render(request,'user_app/profile.html')
@login_required  
def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if pass1 !=None and pass1 !="":
            user.set_password(pass1)
        user.save()


        return redirect('profile')