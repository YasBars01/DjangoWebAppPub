from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.
def register(request):
    # if we receive a POST data, we create a UserRegistrationForm(request.POST)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # hash password
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')  # flash message
            return redirect('login')
    else:
        # we are creating a empty form for the register.html initial view
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # if form is submitted, possibly with new data
    if request.method == 'POST':
        # request.POST - get data from POST
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # if not valid, do not save data
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            # add here instead of letting it fall to render request below
            # avoid POST GET REDIRECT pattern, redirect questions when you reload the form
            # "Are you sure you want to reload? data will be re submitted"
            # which means that the browser will try to send another POST request
            # This redirect causes the browser to send a GET request to the same page, and we do not get the message
            return redirect('profile')

    else:
        # on load of the page, populate the page with the data from DB
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)