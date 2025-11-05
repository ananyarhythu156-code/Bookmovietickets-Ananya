from django.urls import path
from.import views

urlpatterns = [
    path('razorpay/<str:uuid>/',views.RazorpayView.as_view(),name='razorpay'),
    path('payment_verify/',views.PaymentVerify.as_view(),name='payment_verify')

]