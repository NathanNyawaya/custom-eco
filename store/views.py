from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder


def ads(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['cartItems']

	products = Product.objects.all()
	category = Category.objects.all()
	context = {'products':products, 'cartItems':cartItems, 'category': category}
	return render(request, 'store/ads.html', context)

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

# product details
def product_details(request, id):
	data = cartData(request)
	cartItems = data['cartItems']
	product = Product.objects.get(id=id)
	context = {
		"product": product,
		'cartItems': cartItems
	}
	return render(request, 'store/details.html', context)

# category list
# def product_details(request, id):
# 	# category = Category.objects.get(id=cat_id)
# 	product = Product.objects.get(id=id)
# 	context = {
# 		"product": product
# 	}
# 	return render(request, 'store/details.html', context)

def search(request):
	data = cartData(request)
	cartItems = data['cartItems']
	q=request.GET.get("q")
	products = Product.objects.filter(name__icontains=q)
	
	return render(request, 'store/search.html', {'products':products, 'cartItems': cartItems})


def category(request, cat_id):
	data = cartData(request)
	cartItems = data['cartItems']
	category = Category.objects.get(id=cat_id)
	products = Product.objects.filter(category=category).order_by('-id')
	return render(request, 'store/category.html', {'products': products, 'cartItems': cartItems})