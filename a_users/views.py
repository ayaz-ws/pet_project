from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail

from .models import Profile
from .forms import ProfileForm

from a_users.tasks import send_verification_email

@login_required
def send_email(request, profile_uuid):
    profile = get_object_or_404(Profile, verify_uuid=profile_uuid)
    if request.user != profile.user:
        return redirect("home")
    
    if not profile.is_verify:
        verify_url = request.build_absolute_uri(reverse("verify", kwargs={"profile_uuid": profile.verify_uuid}))
        send_verification_email.delay(profile_uuid, verify_url)
        return HttpResponse("Сообщение отправлено. Проверьте свой почтовый ящик")


@login_required
def verify(request, profile_uuid):
    profile = get_object_or_404(Profile, verify_uuid=profile_uuid)
    if request.user != profile.user:
        return redirect("home")

    if request.method == "POST":
        if not profile.is_verify:
            profile.is_verify = True
            profile.save()
        return redirect("profile", username=profile.user.username)

   
    if not profile.is_verify:
        verify_url = request.build_absolute_uri(reverse("verify", kwargs={"profile_uuid": profile.verify_uuid}))
        subject = 'Подтверждение email на сайте "Django Pet Project"'
        message = f'Здравствуйте, для подтверждения своего прфоиля вам необходимо перейти по ссылке {verify_url}'
        from_email = "ayazba@yandex.ru"
        recipient_list = [profile.user.email]
        send_mail(subject, message, from_email, recipient_list)
    
    return render(request, "a_users/verify.html", {"profile": profile})
    


@login_required
def users(request):
    profiles = Profile.objects.all().exclude(user=request.user)
    return render(request, "a_users/users.html", {"profiles": profiles})


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return render(request, "403.html", status=403)
    profile = get_object_or_404(Profile, user=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "a_users/profile_edit.html", {"form": form})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, "a_users/profile_view.html", {"profile": profile})
