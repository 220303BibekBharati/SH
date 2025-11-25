from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart, CartItem
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def order_create(request):
    # Use a DB transaction and lock the cart row to prevent duplicate orders from double submissions
    with transaction.atomic():
        try:
            cart = Cart.objects.select_for_update().get(user=request.user)
        except Cart.DoesNotExist:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart:cart_detail')

        if not cart.items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart:cart_detail')

        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in cart.items.select_related('product').all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity
                    )
                # Clear cart after copying items to the order
                cart.items.all().delete()
                return redirect('payments:process', order_id=order.id)
        else:
            form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@staff_member_required
def orders_monitor(request):
    return render(request, 'orders/monitor.html')