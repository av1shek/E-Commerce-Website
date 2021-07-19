from django.shortcuts import render
from django.urls import reverse  
from django.db.models import Q
from .models import Product, Orders, Message, OrderStatus, Cart
from accounts.models import User, Customer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
import smtplib
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from PayTm import Checksum
from winter.settings import MERCHANT_KEY, MID

orderObj = None


# Display the home page after fetching products
# from Product table according to search query if searched
# else all products
# @login_required
def index(request):
    products = Product.objects.all()
    if(request.method=="GET"):
        query = request.GET.get('query', '')
        products = Product.objects.filter(Q(product_name__icontains=query) | Q(tagline__icontains=query) | Q(desc__icontains=query))

    no_of_product_in_a_page = 4
    n = len(products)
    nSlides = n//no_of_product_in_a_page + 1
    # Django pagination automatically handles pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, no_of_product_in_a_page)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    params = {'no_of_slides': nSlides, 'range': range(1, nSlides+1), 'itemcount': n, 'items': items}
    return render(request, 'shop/index.html', params)


# Display product details of selected product
def product_details(request, myid):
    # Fetch the product using id
    product = Product.objects.filter(id=myid)
    params = {}
    params['product'] = product[0]
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            cart = Cart.objects.get(customer=customer)
            params['cart'] = cart.items_json
        except Exception as e:
            print(e)
    return render(request, 'shop/product_detail.html', params)

@login_required
def cart_update(request):
    json_data = json.loads(request.body.decode("utf-8"))
    print(json_data)
    params = {}
    try:
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user = user)
        cart = Cart.objects.get(customer=customer)
        cart.items_json = json.dumps(json_data);
        cart.save()
        params['success'] = True
    except:
        params['success'] = False
    return HttpResponse(json.dumps(params), content_type="application/json")


# Display cart
@login_required
def cart(request):
    params = {}
    params['isCartEmpty'] = False
    try:
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user = user)
        cart = Cart.objects.get(customer=customer)
        print("check ----------- ",cart.items_json)
        if cart.items_json == '' or cart.items_json == '{}':
            params['isCartEmpty'] = True
        else:
            params['cart'] = cart.items_json
    except Exception as e:
        params['error'] = e
    return render(request, 'shop/cart.html', params)


# Utility function which will accept post request generated
# from javascript file and return the available qunatity of requested
# product id after checking data
# @csrf_exempt
@login_required
def checkdb(request):
    data = json.loads(request.body.decode("utf-8"))
    id = int(data['id'])
    types = data['type']
    qnty = find_qnty(id, types)
    return HttpResponse(qnty)

# Generate receipt
@login_required
def receipt(request, orderid):
    order = Orders.objects.filter(order_id=int(orderid.split('-')[1]))[0]
    items_json = json.loads(order.items_json)
    customer_name = order.fname + " " + order.lname
    address = order.address
    email = order.email
    totalprice =0
    for item in items_json.values():
        totalprice += int(item[2]) * int(item[3])
    products = {'name': customer_name, 'address': address, 'email': email, 'orderid': orderid, 'items_json': items_json, 'grandtotal': totalprice }
    return render(request, 'shop/receipt.html', products)


# Store the message sent by customer in to database
def contact(request):
    if (request.method == "POST"):
        name = request.POST.get('name', 'default')
        email = request.POST.get('email', 'default')
        msg = request.POST.get('message', 'default')
        msgObj = Message(name=name, email=email, message=msg)
        msgObj.save()
        thank = True
        try:
            sendEmail('navodayanabhishek@gmail.com', msg)
        except Exception as e:
            print(e)
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


# Gives the order status after fetching from database
@login_required
def track(request):
    if (request.method == "POST"):
        try:
            orderid = request.POST.get('orderid', '')
            orderid = int(orderid[3:])
            message = OrderStatus.objects.filter(orderid=orderid)[0].orderstatus
        except Exception as e:
            message = "Invalid Order Id"

        thank = True
        return render(request, 'shop/track.html', {'thank': thank, 'message': message})
    return render(request, 'shop/track.html')


def getOrderId():
    with open("media/shop/orderid.txt","r") as f:
        a = int(f.read())
    with open("media/shop/orderid.txt","w") as f:
        f.write(str(a+1))
    return a



# Updates the product database

def updateProductDb(id, types, qnty):
    product = Product.objects.filter(id=id)[0]
    if types == 'sblue':
        product.sblue = product.sblue - qnty
    elif types == 'mblue':
        product.mblue = product.mblue - qnty
    elif types == 'lblue':
        product.lblue = product.lblue - qnty
    elif types == 'sblack':
        product.sblack = product.sblack - qnty
    elif types == 'mblack':
        product.mblack = product.mblack - qnty
    elif types == 'lblack':
        product.lblack = product.lblack - qnty
    product.save()


# Returns the qnty available in database
def find_qnty(id, types):
    product = Product.objects.filter(id=id)[0]
    if types == 'sblue':
        return product.sblue
    elif types == 'mblue':
        return product.mblue
    elif types == 'lblue':
        return product.lblue
    elif types == 'sblack':
        return product.sblack
    elif types == 'mblack':
        return product.mblack
    elif types == 'lblack':
        return product.lblack

def sendEmail(to, content):
    # It sends an email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('singh_821916@student.nitw.ac.in','your-password-here')
    server.sendmail('singh_821916@student.nitw.ac.in', to, content)
    server.close()

# This is for paytm payment integration
@csrf_exempt
def handlerequest(request):
    global orderObj
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    checksum = ''
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            orderObj.save()
            # Create entry in order status table
            orderstatus = OrderStatus(orderid=orderObj.order_id, orderstatus="Order Recieved just now and sent for packing.")
            orderstatus.save()
            print("printing itmes json", orderObj.items_json, " and its type", type(orderObj.items_json))
            mydict = json.loads(orderObj.items_json)
            for key in mydict:
                product_id = mydict[key][6]
                types = mydict[key][7]
                prdouct_qnty = mydict[key][2]
                # Update the quantity of products in products database which is ordered
                # (i.e decrease the amount of quantity )
                updateProductDb(product_id, types, prdouct_qnty)
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})



# Handle the checkout when paytm payment integration
# when merchant id and key is available uncomment this comment the
# the function defined above with same
@login_required
def checkout(request):
    if(request.method=="POST"):
        global orderObj
        itemsjson = request.POST.get('itemsjson', 'default')
        fname = request.POST.get('fname', 'default')
        lname = request.POST.get('lname', 'default')
        branch = request.POST.get('branch', 'default')
        reg_id = request.POST.get('reg_id', 'default')
        mobno = request.POST.get('mobno', 'default')
        email = request.POST.get('email', 'default')
        address = request.POST.get('address1', 'default') + " " + request.POST.get('address2', 'default')
        city = request.POST.get('city', 'default')
        zip_code = request.POST.get('zip_code', 'default')
        state = request.POST.get('state', 'default')
        comment = request.POST.get('comment', 'default')
        items_json = json.loads(itemsjson)
        # print("item json is", items_json, "and its type is ", type(items_json))
        totalprice = 0
        for item in items_json.values():
            totalprice += int(item[2]) * int(item[3])

        # print("total price is ", totalprice)
        order_id = getOrderId()
        orderObj = Orders(order_id=order_id, items_json=itemsjson, fname=fname, lname=lname, branch=branch, reg_id=reg_id, mobno=mobno, email=email, address=address, city=city, zip_code=zip_code, state=state, comment=comment, amount=totalprice)
        order_id = "WHT-" + str(order_id)
        print(order_id)

        # Request paytm to transfer the amount to your account after payment by
        # change callback url at time of production
        param_dict = {
            'MID': MID,
            'ORDER_ID': str(order_id),
            'TXN_AMOUNT': str(totalprice),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    else:
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user = user)
        cart = Cart.objects.get(customer=customer)
        params = {}
        params['cart'] = cart.items_json
        if cart.items_json == '' or cart.items_json == '{}':
            params['isCartEmpty'] = True
    return render(request, 'shop/checkout.html', params)


def test(request):
    return render(request, 'shop/base.html')