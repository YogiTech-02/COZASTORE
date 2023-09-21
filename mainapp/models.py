from django.db import models

class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=50)
    addressline2 = models.CharField(max_length=50)
    addressline3 = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    pic = models.ImageField(upload_to="uploads") 
    otp = models.IntegerField(default=4002652)

    def __str__(self):
        return self.username+"/"+self.name+"/"+self.email


class Maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    maincategory = models.ForeignKey(Maincategory,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    color = models.CharField(max_length=15)
    size = models.CharField(max_length=10,default="",blank=True,null=True)
    baseprice = models.IntegerField()
    discount = models.IntegerField()
    finalprice = models.IntegerField()
    stock = models.BooleanField(default=True)
    discription = models.TextField()
    pic1 = models.ImageField(upload_to="Pics",default="",blank=True,null=True)
    pic2 = models.ImageField(upload_to="Pics",default="",blank=True,null=True)
    pic3 = models.ImageField(upload_to="Pics",default="",blank=True,null=True)

    def __str__(self):
        return self.name


status = ((0,"Order Place"),(1,"Not Packed"),(2,"Packed"),(3,"Ready to Ship"),(4,"Shipped"),(5,"Out of Delivery"),(6,"Delivered"),(7,"Cancelled"))
mode = ((0,"Cod"),(1,"Net Banking"),(2,"Card"))
payment = ((0,"Pending"),(1,"Done"))
class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    orderstatus = models.IntegerField(choices=status,default=0)
    paymentMode = models.IntegerField(choices=mode,default=0)
    paymentstatus = models.IntegerField(choices=payment,default=0)
    rppid = models.CharField(max_length=50,default="",blank=True,null=True)
    totalamount = models.IntegerField()
    shippingamount = models.IntegerField()
    finalamount = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id)+"/"+self.user.username

class Checkoutproduct(models.Model):
    id = models.AutoField(primary_key=True)
    checkout = models.ForeignKey(Checkout,on_delete=models.CASCADE)
    pid = models.IntegerField(default=None)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    price = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    pic =  models.ImageField()


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username+"/"+self.product.name

status = ((0,"Active"),(1,"Done"))
class ContactUS(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=15)
    subject = models.TextField()
    message = models.TextField()
    status = models.IntegerField(choices=status,default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+"/"+self.name+"/"+self.email

# user = coza
# password = project@002