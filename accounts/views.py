from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
# from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.
# from django.urls import reverse
from django.views.generic import TemplateView

from BlogSite import settings
from accounts.forms import UserRegistrationForm, LoginForm, Reset_Password
from accounts.tokens import generate_token

def home(request):
    return render(request, "demo_home.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('homepage')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('homepage')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('homepage')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('homepage')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('homepage')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.username = username
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to V-LOG !!"
        message = "Hello " + myuser.username + "!! \n" + "Welcome to V-LOG !! \nThank you for visiting my website\n. I have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Rohit Thakur"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email for V-LOG Login!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('login')

    return render(request, "signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request, 'activation_failed.html')




def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('homepage')  # Assuming 'homepage' is the name of your homepage URL pattern
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect('homepage')



def forgot_password(request):
    form = Reset_Password()

    if request.method == 'POST':
        form = Reset_Password(request.POST)
        try:
            if form.is_valid():
                user = User.objects.get(email=request.POST['email'])
                print(user.email)
                user.password = make_password(request.POST['new_password'])
                user.save()
                return redirect('login')

        except User.DoesNotExist:
            # Handle the case when the user with the provided email does not exist
            form.add_error('email', 'User with this email does not exist.')

        except Exception as e:
            # Handle any other exceptions that might occur
            print(f"An error occurred: {e}")
            form.add_error(None, 'An error occurred. Please try again.')

    return render(request, 'password_reset.html', {'form': form})
