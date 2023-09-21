from django.shortcuts import render, HttpResponseRedirect, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randint

def home(Request):
    data = Product.objects.all()
    data = data[::-1]
    data = data[0:16]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(Request, "index.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory})


def shop(Request, mc, sc):
    if (mc == "All" and sc == "All"):
        data = Product.objects.all()
    elif (mc != "All" and sc == "All"):
        data = Product.objects.filter(
            maincategory=Maincategory.objects.get(name=mc))
    elif (mc == "All" and sc != "All"):
        data = Product.objects.filter(
            subcategory=Subcategory.objects.get(name=sc))
    else:
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc))
    data = data[::-1]
    data = data[0:16]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'mc': mc, 'sc': sc})


def pricefilter(Request, mc, sc):
    if (Request.method == "POST"):
        min = Request.POST.get("min")
        max = Request.POST.get("max")
        if (mc == "All" and sc == "All"):
            data = Product.objects.filter(
                finalprice__gte=min, finalprice__lte=max)
        elif (mc != "All" and sc == "All"):
            data = Product.objects.filter(
                finalprice__gte=min, finalprice__lte=max, maincategory=Maincategory.objects.get(name=mc))
        elif (mc == "All" and sc != "All"):
            data = Product.objects.filter(
                finalprice__gte=min, finalprice__lte=max, subcategory=Subcategory.objects.get(name=sc))
        else:
            data = Product.objects.filter(finalprice__gte=min, finalprice__lte=max, maincategory=Maincategory.objects.get(
                name=mc), subcategory=Subcategory.objects.get(name=sc))
        # data = Product.objects.filter()
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'mc': mc, 'sc': sc})
    else:
        return HttpResponseRedirect("/shop/All/All/")


def sortfilter(Request, mc, sc):
    if (Request.method == "POST"):
        sort = Request.POST.get("sort")
        if (sort == "newest"):
            sort = "id"
        elif (sort == "HTOL"):
            sort = "finalprice"
        else:
            sort = "-finalprice"
        if (mc == "All" and sc == "All"):
            data = Product.objects.all().order_by(sort)
        elif (mc != "All" and sc == "All"):
            data = Product.objects.filter(
                maincategory=Maincategory.objects.get(name=mc)).order_by(sort)
        elif (mc == "All" and sc != "All"):
            data = Product.objects.filter(
                subcategory=Subcategory.objects.get(name=sc)).order_by(sort)
        else:
            data = Product.objects.filter(maincategory=Maincategory.objects.get(
                name=mc), subcategory=Subcategory.objects.get(name=sc)).order_by(sort)
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'mc': mc, 'sc': sc})

    else:
        return HttpResponseRedirect("/shop/All/All/")


def productDetail(Request, num):
    data = Product.objects.get(id=num)
    maincategory = Maincategory.objects.all()
    return render(Request, "product-detail.html", {'data': data, 'maincategory': maincategory})


def search(Request):
    if (Request.method == "POST"):
        search = Request.POST.get("search")
        data = Product.objects.filter(Q(name__icontains=search) | Q(
            color__icontains=search) | Q(discription__icontains=search))
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory})

@login_required(login_url="/login/")
def checkout(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
    return render(Request,"checkout.html",{"buyer":buyer})


def blog(Request):
    return render(Request, "blog.html")


def about(Request):
    return render(Request, "about.html")


def contact(Request):
    if(Request.method=="POST"):
        c = ContactUS()
        c.name = Request.POST.get("name")
        c.phone = Request.POST.get("phone")
        c.email = Request.POST.get("email")
        c.subject = Request.POST.get("subject")
        c.message = Request.POST.get("message")
        c.save()
        messages.success(Request,"Thanks to Share You Query With Us.Our Team Will Contact You!!")
    return render(Request, "contact.html")


def loginpage(Request):
    if (Request.method == "POST"):
        username = Request.POST.get("username")
        password = Request.POST.get("password")
        user = authenticate(username=username, password=password)
        if (user is not None):
            login(Request, user)
            if (user.is_superuser):
                return HttpResponseRedirect("/admin")
            else:
                return HttpResponseRedirect("/profile")
        else:
            messages.error(Request, "Invalid Username and Password!")
    return render(Request, "login.html")


def logoutpage(Request):
    logout(Request)
    return HttpResponseRedirect("/login")


def signuppage(Request):
    if (Request.method == "POST"):
        name = Request.POST.get("name")
        username = Request.POST.get("username")
        email = Request.POST.get("email")
        phone = Request.POST.get("phone")
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if (password == cpassword):
            try:
                user = User(username=username)
                user.set_password(password)
                user.save()
                buyer = Buyer()
                buyer.name = name
                buyer.username = username
                buyer.email = email
                buyer.phone = phone
                buyer.password = password
                buyer.save()
                subject = 'Account Created -Team CozaStore'
                message = "Thanks to Create an Account with us! Now You can Buy letest Products"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [buyer.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/login")
            except:
                messages.error(Request, "Username Already Exist!")
        else:
            messages.error(Request, "password don't match")
    return render(Request, "signup.html")


@login_required(login_url="/login/")
def profilepage(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
    return render(Request, "profile.html", {'buyer': buyer})


@login_required(login_url="/login/")
def update_profile(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        if (Request.method == "POST"):
            buyer.name = Request.POST.get("name")
            buyer.email = Request.POST.get("email")
            buyer.phone = Request.POST.get("phone")
            buyer.addressline1 = Request.POST.get("addressline1")
            buyer.addressline2 = Request.POST.get("addressline2")
            buyer.addressline3 = Request.POST.get("addressline3")
            buyer.pin = Request.POST.get("pin")
            buyer.city = Request.POST.get("city")
            buyer.state = Request.POST.get("state")
            if (Request.FILES.get("pic")):
                buyer.pic = Request.FILES.get("pic")
            buyer.save()
            return HttpResponseRedirect("/profile")
    return render(Request, "update-profile.html", {'buyer': buyer})

def addtocart(Request,num):
    p = Product.objects.get(id=num)
    cart = Request.session.get("cart",None)
    if(cart):
        if(str(p.id) in cart):
            item = cart[str(p.id)]
            item['qty']=item['qty']+1
            item['total']=item['total']+p.finalprice
            cart[str(p.id)]=item
        else:
            cart.setdefault(str(p.id),{"name":p.name,"color":p.color,"size":p.size,"price":p.finalprice,"qty":1,"total":p.finalprice,"pic":p.pic1.url})
    else:
        cart = {str(p.id):{"name":p.name,"color":p.color,"size":p.size,"price":p.finalprice,"qty":1,"total":p.finalprice,"pic":p.pic1.url}}
    Request.session['cart']=cart
    total = 0
    for value in cart.values():
        total = total+value['total']
    if(total<1000 and total>0):
        shipping = 250
    else:
        shipping = 0
    Request.session['total']=total
    Request.session['shipping']=shipping
    Request.session['final']=total+shipping
    return HttpResponseRedirect("/cart/")

@login_required(login_url="/login/")
def cart(Request):
    cart = Request.session.get("cart",None)
    items = []
    if(cart):
        for key, value in cart.items():
            value.setdefault('id',key)
            items.append(value)
    total = Request.session.get('total',0)
    shipping = Request.session.get('shipping',0)
    final = Request.session.get('final',0)
    return render(Request,"cart.html",{"cart":items,'total':total,'shipping':shipping,'final':final})

def updatecart(Request,id,op):
    cart = Request.session.get("cart",None)
    if(cart and id in cart):
        item = cart[id]
        if(op=="dec" and item['qty']==1):
            pass
        elif(op=="dec"):
            item["qty"]=item["qty"]-1
            item["total"]=item["total"]-item["price"]
        else:
            item["qty"]=item["qty"]+1
            item["total"]=item["total"]+item["price"]
        cart[id]=item
        Request.session["cart"]=cart
        total = 0
        for value in cart.values():
            total = total+value['total']
        if(total<1000 and total>0):
            shipping = 250
        else:
            shipping = 0
        Request.session['total'] = total
        Request.session['shipping']=shipping
        Request.session['final']=total+shipping
    return HttpResponseRedirect("/cart/",)

def deletecart(Request,id):
    cart = Request.session.get("cart",None)
    if(cart and id in cart):
        del cart[id]
        Request.session["cart"]=cart
        total = 0
        for value in cart.values():
            total =  total+value['total']
        if(total<1000 and total>0):
            shipping = 250
        else:
            shipping = 0
        Request.session['total'] = total
        Request.session['shipping'] = shipping
        Request.session['final'] = total+shipping
    return HttpResponseRedirect("/cart/")

@login_required(login_url="/login/")
def placeorder(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin")
    else:
        total = Request.session.get("total")
        if(total):
            shipping = Request.session.get("shipping",0)
            final = Request.session.get("final",0)
            buyer = Buyer.objects.get(username=Request.user.username)
            checkout = Checkout()
            checkout.user = buyer
            checkout.totalamount = total
            checkout.shippingamount = shipping
            checkout.finalamount = final
            checkout.save()

            cart = Request.session.get("cart",None)
            for key,value in cart.items():
                checkoutproduct = Checkoutproduct()
                checkoutproduct.checkout = checkout
                checkoutproduct.pid = int(key)
                checkoutproduct.name = value['name']
                checkoutproduct.color = value['color']
                checkoutproduct.size = value['size']
                checkoutproduct.price = value['price']
                checkoutproduct.qty = value['qty']
                checkoutproduct.total = value['total']
                checkoutproduct.pic = value['pic']
                checkoutproduct.save()
            Request.session['cart'] = {}
            Request.session['total'] = 0
            Request.session['shipping'] = 0
            Request.session['final'] = 0
            return HttpResponseRedirect("/confirmation/")
        else:
            return HttpResponseRedirect("/cart/")

@login_required(login_url="/login/")
def confirm(Request):
    username = Request.user.username
    if(username):
        try:
            buyer = Buyer.objects.get(username=username)
            subject = 'Order has been Placed -Team CozaStore'
            message = "Thanks to shopping with US! Your Order has been Placed! Now You can Track Your Order."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [buyer.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(Request,"confirmation.html")
        except:
            return HttpResponseRedirect("/shop/All/All")
    else:
        return HttpResponseRedirect("/shop/All/All")

@login_required(login_url="/login/")
def addtowishlist(Request,num):
    user = User.objects.get(username=Request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        product = Product.objects.get(id=num)
        try:
            wishlist = Wishlist.objects.get(user=buyer,product=product)
        except:    
            wish = Wishlist()
            wish.user = buyer
            wish.product = product
            wish.save()
        return HttpResponseRedirect("/wishlist/")
    
@login_required(login_url="/login/")
def wishlist(Request):
    user = User.objects.get(username=Request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        wishlist = Wishlist.objects.filter(user=buyer)
    return render(Request,"wishlist.html",{'wishlist':wishlist})


@login_required(login_url="/login/")
def deletewishlist(Request,num):
    user = User.objects.get(username=Request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        try:
            wishlist = Wishlist.objects.filter(user=buyer,id=num)
            wishlist.delete()
        except:
            pass
        return HttpResponseRedirect("/wishlist")
    
def forgotpw1(Request):
    if(Request.method=="POST"):
        username = Request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin")
            else:
                Request.session['resetuser']=username
                num = randint(100000,999999)
                buyer = Buyer.objects.get(username=username)
                buyer.otp = num
                buyer.save()
                subject = 'OTP for Reset-Password -Team CozaStore'
                message = "OTP for Reset-password is "+str(num)+"\nNever Share Your OTP with anyone"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [buyer.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/forgotpw-2/")
        except:
            messages.error(Request,"Invalid Username")
    return render(Request,"forgotpw-1.html")


def forgotpw2(Request):
    resetuser = Request.session.get('resetuser',None)
    if(Request.method=="POST" and resetuser):
        otp = Request.POST.get("otp")
        try:
            buyer = Buyer.objects.get(username=resetuser)
            if(buyer.otp == int(otp)):
                Request.session['otp']=otp
                return HttpResponseRedirect("/forgotpw-3/")
            else:
                messages.error(Request,"Invalid OTP")
        except:
            messages.error(Request,"Invalid username")
    return render(Request,"forgotpw-2.html")

def forgotpw3(Request):
    otp = Request.session.get("otp",None)
    if(otp):
        if(Request.method == "POST"):
            resetuser = Request.session.get("resetuser",None)
            if(resetuser and otp):
                buyer = Buyer.objects.get(username=resetuser)
                if(int(otp) == buyer.otp):
                    password = Request.POST.get("password")
                    cpassword = Request.POST.get("cpassword")
                    if(password!=cpassword):
                        messages.error(Request,"Password and Confirm Password Does't matched! Please write properly")
                    else:
                        user = User.objects.get(username=resetuser)
                        user.set_password(password)
                        user.save()
                        subject = 'Password Reset Successfully -Team CozaStore'
                        message = "Your Password has been Reset Successfully Now You can Login your Account and Buy Products"
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [buyer.email, ]
                        send_mail( subject, message, email_from, recipient_list )
                        del Request.session['resetuser']
                        del Request.session['otp']
                        return HttpResponseRedirect('/login/')
                else:
                    messages.error(Request,"Unauthorised User")                
            else:
                messages.error(Request,"Unauthorised User")
        return render(Request, "forgotpw-3.html")
    else:
        return HttpResponseRedirect("/forgotpw-1/")