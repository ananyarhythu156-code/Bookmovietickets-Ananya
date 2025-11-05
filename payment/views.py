from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from decouple import config
import razorpay

from .models import Payment, Transactions

from ticket.models import Booking    


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        payment_obj = Payment.objects.get(uuid=uuid)

        client = razorpay.Client(auth=(config('RZP_KEY_ID'), config('RZP_KEY_SECRET')))

        data = {
            "amount": int(payment_obj.amount * 100),
            "currency": "INR",
            "receipt": f"rcpt_{str(uuid).replace('-', '')[:30]}"
        }

        payment = client.order.create(data=data)

        rzp_order_id = payment.get('id')

        amount = payment.get('amount')

        Transactions.objects.create(payment=payment_obj, rzp_order_id=rzp_order_id, amount=amount)

        data = {
            'RZP_KEY_ID': config('RZP_KEY_ID'),
            'amount': amount,
            'order_id': rzp_order_id
        }

        return render(request, 'payment/razorpay.html', context=data)
    
    


@method_decorator(csrf_exempt, name='dispatch')
class PaymentVerify(View):

    def post(self, request, *args, **kwargs):

        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        client = razorpay.Client(auth=(config('RZP_KEY_ID'), config('RZP_KEY_SECRET')))

        
        paid = client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
       

        transaction = Transactions.objects.get(rzp_order_id=razorpay_order_id)

        if paid:

            transaction.status = 'Success'

            transaction.payment.status = 'Success'

        else:
            transaction.status = 'Failed'

            transaction.payment.status = 'Failed'

        transaction.transaction_at = timezone.now()

        transaction.rzp_payment_id = razorpay_payment_id

        transaction.rzp_signature = razorpay_signature

        transaction.save()

        transaction.payment.paid_at = timezone.now()

        transaction.payment.save()

        if transaction.status == 'Success':

            messages.success(request, '🎟️ Ticket Booked Successfully!')

            transaction.payment.booking.is_confirmed = True

            transaction.payment.booking.save()

            return redirect('booking_confirmation', uuid=transaction.payment.booking.uuid)

        else:

            messages.error(request, '❌ Payment Failed. Please try again.')

        return redirect('home')
