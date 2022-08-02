from io import BytesIO

from PIL import Image
from django.core.files import File
from django.db import models
# Create your models here.
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from config import settings
from django.contrib.postgres.fields import ArrayField

from clients.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование категории', null=True)
    slug = models.CharField(max_length=200, null=True)
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория-родитель',
                                        blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Photo(models.Model):
    file = models.ImageField(upload_to='products/images', max_length=500, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='photo')

    def __str__(self):
        return f'{self.id} {self.product.name}'

    class Meta:
        verbose_name = "Фотo"
        verbose_name_plural = "Фото"

    def save(self, *args, **kwargs):
        im = Image.open(self.file)
        im_io = BytesIO()
        im.save(im_io, im.format, optimize=True, quality=40)
        new_image = File(im_io, name=self.file.name)
        self.file = new_image
        super().save(*args, **kwargs)

STATUS = [
    ('Active', 'Active'),
    ('Sold', 'Sold'),
    ('Publication off', 'Publication off')
]

class Product(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Sold', 'Sold'),
        ('On moderation', 'On moderation'),
        ('Publication off', 'Publication off')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Подкатегория',
                                 related_name='product')
    manufacturer = models.CharField(max_length=200, verbose_name='Производитель', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Наименование товара', null=True)
    price = models.IntegerField(default=0, verbose_name='Цена')
    description = models.CharField(max_length=2000, verbose_name='Описание', null=True, blank=True)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры', blank=True)
    favorites_count = models.IntegerField(default=0, verbose_name='Избранное', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано', blank=True)
    location = models.CharField(max_length=2000, verbose_name='Местоположение объявления', null=True, blank=True)
    parent_product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт-родитель', blank=True,
                                       null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')

    def __str__(self):
        return f'{self.id} {self.user.email} {self.name}'

    def to_json(self):
        return {
            'id': self.id,
            'user': self.user,
            'category': self.category,
            'manufacturer': self.manufacturer,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'views_count': self.views_count,
            'favorites_count': self.favorites_count,
            'created': self.created,
            'location': self.location,
            'parent_product': self.parent_product,
            'status': self.status,
        }

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class AssetsDataType(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'Тип данных характеристики'
        verbose_name_plural = 'Типы данных характеристик'

class Asset(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование характеристики', null=True)
    measure_units = models.CharField(max_length=50, verbose_name='Единицы измерения', null=True, blank=True)
    slug = models.CharField(max_length=200, null=True)
    data_type = models.ForeignKey(AssetsDataType, on_delete=models.CASCADE, verbose_name='Тип данных', null=True, blank=True)
    options = ArrayField(
        models.CharField(max_length=20, verbose_name='Вариант значения', blank=True, null=True)
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class AssetTemplate(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='Характеристика')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.category.name} {self.asset.name}'

    class Meta:
        verbose_name = 'Набор характеристик для категории'
        verbose_name_plural = 'Наборы характеристик для категорий'



class ValueAsset(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='Характеристика')
    value = models.CharField(max_length=512, verbose_name='Значение характеристики', null=True, blank=True)

    def __str__(self):
        return f'{self.product.id} {self.asset.name} {self.value}'

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значение характеристики'


class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name='favortie_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='favortie_user')

    def __str__(self):
        return f'{self.product.id} {self.user.email}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


@receiver(post_save, sender=Favorites)
def create_favorites(sender, instance, created, **kwargs):
    if created:
        instance.product.favorites_count += 1
        instance.product.save()


@receiver(pre_delete, sender=Favorites)
def delete_favorites(sender, instance, **kwargs):
    instance.product.favorites_count -= 1
    instance.product.save()


class History(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name='history_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='history_user')
    watched = models.DateTimeField(auto_now_add=True, verbose_name='Время просмотра', null=True)

    def __str__(self):
        return f'{self.product.id} {self.user.email}'

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'История'


@receiver(post_save, sender=History)
def create_favorites(sender, instance, created, **kwargs):
    if created:
        instance.product.views_count += 1
        instance.product.save()
