# # views.py

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import PhoneNumberForm
# from .models import OTP
# from twilio.rest import Client
# import random

# def send_otp(request):
#     if request.method == 'POST':
#         form = PhoneNumberForm(request.POST)
#         if form.is_valid():
#             phone_number = form.cleaned_data['phone_number']
#             otp_value = str(random.randint(100000, 999999))
            
#             # Send OTP via Twilio
#             client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#             client.messages.create(
#                 body=f'Your OTP is {otp_value}',
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=phone_number
#             )
            
#             # Save OTP
#             otp_instance = OTP.objects.create(user=request.user, otp=otp_value)
#             request.session['otp_id'] = otp_instance.id
            
#             messages.success(request, 'OTP sent successfully!')
#             return redirect('verify_otp')
#     else:
#         form = PhoneNumberForm()
#     return render(request, 'send_otp.html', {'form': form})

# def verify_otp(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         otp_id = request.session.get('otp_id')
#         try:
#             otp_instance = OTP.objects.get(id=otp_id)
#             if otp_instance.otp == entered_otp and not otp_instance.is_expired():
#                 messages.success(request, 'OTP verified successfully!')
#                 otp_instance.delete()  # Delete OTP after verification
#                 return redirect('success_page')  # Redirect to a success page
#             else:
#                 messages.error(request, 'Invalid or expired OTP.')
#         except OTP.DoesNotExist:
#             messages.error(request, 'OTP session expired.')
#     return render(request, 'verify_otp.html')




# # models.py

# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

# class OTP(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(default=timezone.now)

#     def is_expired(self):
#         return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
