from django.db import models
# Create your models here.
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from clients.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование категории', null=True)
    slug = models.CharField(max_length=200, null=True)
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория-родитель')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Подкатегория',
                                 related_name='product')
    manufacturer = models.CharField(max_length=200, verbose_name='Производитель', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Наименование товара', null=True)
    price = models.IntegerField(default=0, verbose_name='Цена')
    description = models.CharField(max_length=2000, verbose_name='Описание', null=True, blank=True)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    favorites_count = models.IntegerField(default=0, verbose_name='Избранное')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    location = models.CharField(max_length=2000, verbose_name='Местоположение объявления', null=True, blank=True)
    parent_product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт-родитель')

    def __str__(self):
        return f'{self.user.email} {self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Asset(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование характеристики', null=True)
    slug = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


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
def create_favorites(sender, instance, **kwargs):
    instance.product.favorites_count -= 1
    instance.product.save()


class History(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name='history_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='history_user')

    def __str__(self):
        return f'{self.product.id} {self.user.email}'

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'История'
