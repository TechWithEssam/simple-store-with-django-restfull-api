from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


User = settings.AUTH_USER_MODEL


class Category(models.Model) :
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(blank=True, null=True, unique=True)
    def __str__(self) :
        return self.name
    
    def save(self, *args, **kwargs) :
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Brand(models.Model) :
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(blank=True, null=True, unique=True)
    def __str__(self) :
        return self.name
    def save(self, *args, **kwargs) :
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


CATEGORY_GENDER = (
    ("male","male"),
    ("female","female"),
    ("children", "children")
)


class Product(models.Model) :
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender = models.CharField(choices=CATEGORY_GENDER, blank=True, null=True, max_length=20)
    discound = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    inventory_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self) :
        return str(self.name)
    @property
    def new_price_after_discound(self) :
        if self.discound > 0 :
            new_price = self.price - self.price * self.discound / 100
        else :
            new_price = self.price
        return new_price
    def __str__(self) :
        return f"{str(self.name)}"