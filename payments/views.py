from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .models import Payment
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        method = request.POST.get('payment_method')
        if method == 'online':
            # Simulate online payment success
            order.paid = True
            if hasattr(order, 'status'):
                order.status = 'processing'
            order.save()
            Payment.objects.create(
                order=order,
                stripe_charge_id='dummy_charge_id',
                amount=order.get_total_cost()
            )
            messages.success(request, 'Online payment successful! Your order is confirmed.')
        elif method == 'cod':
            # Cash on Delivery: do not mark as paid yet
            if hasattr(order, 'status'):
                order.status = 'pending'
            order.save()
            messages.info(request, 'Order placed with Cash on Delivery. You will pay upon delivery.')
        else:
            messages.error(request, 'Please select a payment method.')
            return redirect('payments:process', order_id=order.id)

        return redirect('orders:order_detail', order_id=order.id)
    else:
        # In real implementation, create Stripe session
        # For now, just render a dummy form
        return render(request, 'payments/process.html', {'order': order})