from django.shortcuts import render, redirect
from .forms import PropertyOwnerSignUpForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render

from django.http import HttpResponse


def home(request):
     return render(request, 'base_generic.html', {})


def property_owner_sign_up(request):
    if request.method == 'POST':
        form = PropertyOwnerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            messages.success(
                request, 'Your sign-up request has been submitted successfully. Please wait for approval.')
            # login(request, user)  # Automatically log the user in
            # Redirect to a success page
            return redirect('property_owner_sign_up_success')
        else:
            messages.error(
                request, 'There was an error with your sign-up. Please try again.')
    else:
        form = PropertyOwnerSignUpForm()

    return render(request, 'property_owner_sign_up.html', {'form': form})


def property_owner_sign_up_success(request):
    return render(request, 'property_owner_sign_up_success.html')
