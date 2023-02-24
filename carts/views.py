from django.shortcuts import render, redirect,get_object_or_404
from productos.models import Producto,Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart= request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Create your views here.
def add_cart(request, product_id):
    product = Producto.objects.get(id = product_id)
    current_user =request.user

    if current_user.is_authenticated:
        #aqui se agregara la logica cuando el usuario esta autenticado
        product_varation = []
        if request.method == 'POST':
            for item in request.POST:
                key =item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_varation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)   
                
                
            if product_varation in ex_var_list:
                
                index = ex_var_list.index(product_varation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item=CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_varation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_varation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product, 
                quantity= 1, 
                user = current_user,
            )
            if len(product_varation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_varation)
            cart_item.save()
        return redirect('cart')
    else:

        product_varation = []
        if request.method == 'POST':
            for item in request.POST:
                key =item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_varation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)   
                
                
            if product_varation in ex_var_list:
                
                index = ex_var_list.index(product_varation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item=CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_varation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_varation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product, 
                quantity= 1, 
                cart = cart,
            )
            if len(product_varation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_varation)
            cart_item.save()
        return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Producto, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = CartItem.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart =cart, id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Producto, id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart =cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_item = None):
    try:
        if request.user.is_authenticated:
            cart_items= CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items= CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (0.19*total)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax':tax,
    }

    return render(request, 'carts/cart.html', context)

@login_required(login_url='login')
def checkout(request,total=0, quantity=0, cart_item = None):    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items= CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (0.19*total)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax':tax,
    }
    return render(request,'productos/checkout.html',context)
