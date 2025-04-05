from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new User instance, but don't save it to the database
            new_user = user_form.save(commit=False)
            # Let Django set the password
            new_user.set_password(user_form.cleaned_data['password'])
            # Now save the User
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request,
                'merlin/register_done.html',
                {
                    'new_user': new_user,
                }
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'merlin/register.html',
        {
            'user_form': user_form,
        }
    )


@login_required
def dashboard(request):
    return render(
        request,
        'merlin/dashboard.html',
        {
            'section': 'dashboard',
        }
    )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'merlin/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )
