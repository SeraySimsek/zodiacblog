from django.db import models
from django.contrib.auth.models import User

# Create your models here.
zodiac_type_choice = (
    ('seçiniz', 'seçiniz'),
    ('koç', 'koç'),
    ('boğa', 'boğa'),
    ('ikizler', 'ikizler'),
    ('yengeç', 'yengeç'),
    ('aslan', 'aslan'),
    ('başak', 'başak'),
    ('terazi', 'terazi'),
    ('akrep', 'akrep'),
    ('yay', 'yay'),
    ('oğlak', 'oğlak'),
    ('kova', 'kova'),
    ('balık', 'balık'))

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null=True)
    job = models.CharField(max_length=100, null=True)
    zodiac = models.CharField(choices=zodiac_type_choice, max_length=25, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    gender_choice = (('E', 'Erkek'),('K', 'Kadın'))
    gender = models.CharField(choices=gender_choice, max_length=10, null=True)
    relationship_choice = (('V','Var'),('Y','Yok'))
    relationship = models.CharField(choices=relationship_choice, max_length=10, null=True)

    def __str__(self):
        return str(self.id) +"-"+self.name+" "+self.lastname

    def register(self):
        self.save()

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property #method değilde attribute olarak ulaşmamızı sağlıyor
    def imageURL(self): #eğer image url exist değilse
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False) #eğer false ise sepete hala product ekleniyor, true ise satın alınmış
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):  # sepetteki total için
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self): #sepetteki kaç tane item varsa onları topluyor
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model): #for creating items to added our order(many to one relationship)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) #single order can have multiple items
    quantity = models.IntegerField(default=0, null=True, blank=True) #kaç tane product var?
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self): #total fiyatımızı veriyor
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Bank(models.Model):
    name_on_card = models.CharField(max_length=200, blank=False, primary_key=True)
    credit_card_number = models.CharField(max_length=16, blank=False)
    expiration = models.CharField(max_length=5, null=False, blank=False)
    cvv = models.CharField(max_length=3, null=False, blank=False)
    balance = models.FloatField(max_length=10, default=1000)

    def __str__(self):
        return self.credit_card_number

class user_type(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    user_type_choice = (('F', 'Falcı'), ('B', 'Burç Yorumcusu'), ('U', 'Kullanıcı'))
    user_type = models.CharField(choices=user_type_choice, max_length=100, null=True)

    def __str__(self):
        return str(self.customer.name) + ' ' + str(self.customer.lastname) + ' (' + str(self.user_type) + ')'

    class Meta:
        verbose_name = 'Kullanıcı Tipi'
        verbose_name_plural = 'Kullanıcı Tipleri'
        ordering = ['user_type']

class FortuneTelling(models.Model):
    from_user = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE, related_name='from_user')
    is_ok = models.CharField(default='N', max_length=1, null=False)
    pic = models.CharField(max_length=15, null=False)
    to_user = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='to_user', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_review = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.from_user.name) + ' ' + str(self.from_user.lastname) + ' ' + str(self.date_added)

    class Meta:
        verbose_name = 'Gönderilen Fal'
        verbose_name_plural = 'Gönderilen Fallar'
        ordering = ['from_user']

class post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(max_length=2000, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='customer')
    date_added = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=25, null=False)
    zodiac_type = models.CharField(default='seçiniz', choices=zodiac_type_choice, max_length=25, null=True)
    post_for = models.ForeignKey(FortuneTelling, null=True, on_delete=models.CASCADE, related_name='post_for', blank=True)

    def __str__(self):
        if self.post_type.__eq__('F'):
            return str(self.post_type) + ': ' + str(self.title)
        else:
            return str(self.post_type) + ' - ' + str(self.zodiac_type) + ': ' + str(self.title)

    class Meta:
        verbose_name = 'Fal/Burç Gönderisi'
        verbose_name_plural = 'Fal/Burç Gönderileri'
        ordering = ['post_type', 'date_added']

class Contact(models.Model):
    comment= models.TextField(max_length=1000, null=True)
    customer =models.ForeignKey(Customer,null=True,on_delete= models.CASCADE)

    def __str__(self):
        return str(self.id)