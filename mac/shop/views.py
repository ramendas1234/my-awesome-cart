from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django import template
import json
MERCHANT_KEY = 'irGqZ0yPpIq0G@JP'
# Create your views here.
# TEST CREDENTIALS FOR PAYTM
# Mobile Number : 7777777777
# Password : Paytm12345
# OTP : 489871

def index(request):
	allProds = []
	catprods = Product.objects.values('category', 'id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prod = Product.objects.filter(category=cat)
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		allProds.append([prod, range(1, nSlides), nSlides])
	params = {'allProds':allProds}

	return render(request, 'shop/index.html', params)
def about(request):
	return render(request, 'shop/about.html')
def contact(request):
	if request.method=="POST":
		name = request.POST.get('name', '')
		email = request.POST.get('email', '')
		phone = request.POST.get('phone', '')
		desc = request.POST.get('desc', '')
		contact = Contact(name=name, email=email, phone=phone, desc=desc)
		contact.save()
	return render(request, 'shop/contact.html')
def tracker(request):
	if request.method == "POST":
		orderId = request.POST.get('orderId','')
		email = request.POST.get('email','')
		try:
			order = Orders.objects.filter(order_id = orderId, email = email)
			if len(order) > 0 :
				update = OrderUpdate.objects.filter(order_id = orderId)
				updates = []
				for item in update:
					updates.append({'text': item.update_desc, 'time': item.timestamp.strftime("%b %d")})
					response = json.dumps([updates, order[0].items_json], default=str)
				return HttpResponse(response)
				
			else:
				return HttpResponse('{}')	
		
		except Exception as e:
			return HttpResponse('{}')
	return render(request, 'shop/tracker.html')
def searchMatch(query, item):
	'''return true only if query matches the item'''
	if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
		return True
	else:
		return False
def search(request):
	query = request.GET.get('search')
	if len(query) < 1:
		params = {'msg': "Please enter search keyword"}
		return render(request, 'shop/search.html',params)
	products = Product.objects.all()
	allProds = [item for item in products if searchMatch(query, item)]
	# for cat in cats:
		# prodtemp = Product.objects.filter(category=cat)
		# prod = [item for item in prodtemp if searchMatch(query, item)]
		# if len(prod) != 0:
			# allProds.append([prod])
	params = {'allProds': allProds, "msg": ""}
	if len(allProds) < 1 :
		params = {'msg': "Sorry no products found"}
	return render(request, 'shop/search.html',params)
def productView(request, myid):
	product = Product.objects.filter(id=myid)
	related_products = Product.objects.filter(category=product[0].category).exclude(pk=myid)
	
	return render(request, 'shop/prodView.html', {'product':product[0],'related_products':related_products})
	
def checkout(request):
	if request.method=="POST":
		validation_error = {}
		items_json = request.POST.get('itemsJson', '')
		amount = request.POST.get('amount', '')
		name = request.POST.get('name', '')
		email = request.POST.get('email', '')
		address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
		city = request.POST.get('city', '')
		state = request.POST.get('state', '')
		zip_code = request.POST.get('zip_code', '')
		phone = request.POST.get('phone', '')
		thank = False
		loaded_json = json.loads(items_json)
		productQtyError = []
		for item in loaded_json:
			productId = int(item.replace("pr",''))
			product = Product.objects.get(pk = productId)
			itemQty = int(loaded_json[item][0])
			if itemQty > product.quantity:
				productQtyError.append(product.product_name+"  is out of quantity")
		
		if len(productQtyError):
			return render(request, 'shop/checkout.html', {'thank':thank, 'product_qty_error':productQtyError})
		if  not items_json:
			validation_error['item_error'] = 'Sorry there have no items for place order'
		if not name:
			validation_error['name_error'] = 'Name required'
		if not email:
			validation_error['email_error'] = 'Email required'
		if not address or address==' ':
			validation_error['address_error'] = 'Address required'
		if not city:
			validation_error['city_error'] = 'City required'
		if not state:
			validation_error['state_error'] = 'State required'
		if not zip_code:
			validation_error['zip_error'] = 'Zip required'
		if not phone:
			validation_error['phone_error'] = 'Phone required'

		if  not bool(validation_error):
			order = Orders(items_json=items_json, amount=amount,name=name, email=email, address=address, city=city,state=state, zip_code=zip_code, phone=phone)
			order.save()
			update = OrderUpdate(order_id = order.order_id, update_desc = 'Order Has been Placed')
			update.save()
			thank = True
			id = order.order_id
			# return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
			# Request paytm to transfer the amount to your account after payment by user
			param_dict = {
			"MID": "voXgAz24422752375062",
			"ORDER_ID": str(order.order_id),
			"CUST_ID": email,
			"TXN_AMOUNT": str(amount),
			"CHANNEL_ID": "WEB",
			"INDUSTRY_TYPE_ID": "Retail",
			"WEBSITE": "WEBSTAGING",
			"CALLBACK_URL": "http://127.0.0.1:8000/shop/handlerequest/"
			}
			param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
			return render(request, 'shop/paytm.html', {'param_dict':param_dict})
		else:
			return render(request, 'shop/checkout.html', {'thank':thank, 'error':validation_error})
	return render(request, 'shop/checkout.html')		
def test(request):
	products = Product.objects.all()
	allProds = []
	catprods = Product.objects.values('category', 'id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prod = Product.objects.filter(category=cat)
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		allProds.append([prod, range(1, nSlides), nSlides])
	
	params = {'allProds':allProds}
	#params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
	return render(request, 'shop/test.html', params)

# THIS FUNCTION IS USE FOR PAYTM HAMDLE REQUEST AFTER PAYMENT

@csrf_exempt
def handlerequest(request):
	# Paytm will send you post request here
	form = request.POST
	response_dict = {}
	for i in form.keys():
		response_dict[i] = form[i]
		if i == 'CHECKSUMHASH':
			checksum = form[i]
	verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
	if verify:
		if response_dict['RESPCODE'] == '01':
			# here we need order id because after order need decrease product quantity
			orderId = response_dict['ORDERID']
			order = Orders.objects.get(pk = orderId)
			items_json = order.items_json
			loaded_json = json.loads(items_json)
			for item in loaded_json:
				productId = int(item.replace("pr",''))
				product = Product.objects.get(pk = productId)
				itemQty = int(loaded_json[item][0])
				remainingQty = product.quantity - itemQty
				product.quantity = remainingQty
				product.save()
			print('order successful')
		else:
			print('order was not successful because' + response_dict['RESPMSG'])	
	return render(request, 'shop/paymentstatus.html', {'response': response_dict})

	
def abc(request):
	return render(request,'shop/abc.html')
