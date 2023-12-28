from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyUserCreationForm, UserEditForm, UserProfileEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def send_activation_email(request, user):
    current_site = get_current_site(request)
    email_subject = "Activate your CP Drills account!"
    email_body = render_to_string("accounts/email_verify.html", {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject,
                         body=email_body,
                         from_email="CP Drills <" + settings.EMAIL_HOST_USER + ">",
                         to=[user.email])

    # EmailThread(email).start()
    email.send(fail_silently=False)


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Email verified. You may log in now.")
        return redirect('sign_in')

    return render(request, 'accounts/activate_failed.html', {"user": user})


def sign_up(request):
    """
    Custom user sign up
    """

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal

            user.is_active = False

            user.userprofile.country = form.cleaned_data.get('country')
            user.userprofile.codeforces_handle = form.cleaned_data.get('codeforces_handle')
            user.userprofile.gender = form.cleaned_data.get('gender')
            user.userprofile.save()  # Saving UserProfile object
            user.save()  # Saving User object

            send_activation_email(request, user)

            # login(request, user)

            messages.success(request,
                             "We have sent you an email to verify your account. Don't forget to check spam folders!")
            return redirect('home')
    else:
        form = MyUserCreationForm()

    return render(request, 'accounts/sign_up.html', {'form': form})


def user_logout(request):
    """
    View for logging users out.
    """

    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


def sign_in(request):
    """
    Standard user sign in
    """

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request,
                                 'Welcome, ' + user.username + '! Please note that the training pages are not yet optimised for smaller screens.')
                return redirect('train')
        else:
            username = form.cleaned_data.get('username')
            user_obj = User.objects.filter(username=username)

            if user_obj.exists():
                if not user_obj[0].is_active:
                    messages.error(request, 'Please check your inbox and verify your email. A mail was sent again.')
                    send_activation_email(request, user_obj[0])
                    return redirect('sign_in')
            else:
                messages.error(request, "Invalid username...")
                return redirect('sign_in')

            messages.error(request, 'Invalid password...')
            return redirect('sign_in')

    form = AuthenticationForm()
    return render(request, "accounts/sign_in.html", {"form": form})


@login_required
def profile_edit(request):
    """
    Lets user edit their profile.
    """

    if request.method == "POST":
        user_edit_form = UserEditForm(request.POST, instance=request.user)
        userprofile_edit_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)

        if user_edit_form.is_valid() and userprofile_edit_form.is_valid():
            user_edit_form.save()
            userprofile_edit_form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "An error occurred.")

        return redirect('profile_edit')

    user_edit_form = UserEditForm(instance=request.user)
    userprofile_edit_form = UserProfileEditForm(instance=request.user.userprofile)
    return render(request, "accounts/profile_edit.html",
                  {"user_form": user_edit_form, "userprofile_form": userprofile_edit_form})
