from django.db import models
from django.contrib.auth.models import User




def product_image_directory_path(instance: 'Product', filename: str) -> str:
    return 'product/product_{pk}/image/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Image(models.Model):
    src = models.ImageField(upload_to=product_image_directory_path)
    alt = models.CharField(max_length=255)

    def __str__(self):
        return self.alt


class Specification(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    subcategories = models.ManyToManyField(Subcategory)

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    rate = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return self.author


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    count = models.IntegerField()
    date = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    fullDescription = models.TextField()
    freeDelivery = models.BooleanField()
    rating = models.FloatField()
    images = models.ManyToManyField(Image)
    tags = models.ManyToManyField(Tag)
    reviews = models.ManyToManyField(Review)
    specifications = models.ManyToManyField(Specification)
    sale = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Sales(models.Model):
    price = models.FloatField(default=0)
    salePrice = models.FloatField(default=0)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    title = models.CharField(max_length=255)
    images = models.ManyToManyField(Image)
    currentPage = models.IntegerField()
    lastPage = models.IntegerField()

    def __str__(self):
        return self.title


class OrderProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    count = models.IntegerField()
    date = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    freeDelivery = models.BooleanField(default=True)
    images = models.ManyToManyField(Image)
    tags = models.ManyToManyField(Tag)
    reviews = models.ManyToManyField(Review)
    rating = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title



class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.TextField()
    deliveryType = models.TextField(null=True, blank=True)
    paymentType = models.TextField(null=True, blank=True)
    totalCost = models.FloatField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    city = models.TextField()
    address = models.TextField()
    products = models.ManyToManyField(OrderProduct)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):
        products_titles = ', '.join([product.title for product in self.products.all()])
        return products_titles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.TextField()
    avatar = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.fullName





class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    code = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Basket(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField()
