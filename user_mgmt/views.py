from django.shortcuts import render, get_object_or_404
from .models import User, Customer

def user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'user_details.html', {'user': user})

def customer_profile(request, user_id):
    customer = get_object_or_404(Customer, user__userID=user_id)
    return render(request, 'customer_profile.html', {'customer': customer})
