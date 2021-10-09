from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.contrib.auth import get_user_model


"""
Register
=====
name, cellphone, password, address_list, about

Reserve
=====
name, cellphone, date, time, person_numbers, notes

Posts_Category
====
title, slug, sort_id

Tag
====
title, slug

Menu_Category
====
title, slug, sort_id

Post
====
title, slug, content, author, created_at, published_at, photo, views, tags, published, updated_at, sort_id

Item_menu
=====
category, title, slug, recipe, created_at, updated_at, photo, tags, price, promo, published_slider, published, 
item_number,in_cart, sort_id

Comment
===
created_at, updated_at, parent_obj, content   
"""


class PostsCategory(models.Model):

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('craft:category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория Поста'
        verbose_name_plural = 'Категории Поста'
        ordering = ['title']


class Tag(models.Model):

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True,)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('craft:tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['title']


class Post(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True,)
    content = models.TextField(blank=True, verbose_name='Текст')
    # author = models.ForeignKey(verbose_name='Автор', on_delete=models.CASCADE),
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Созданно')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменение')
    published_at = models.BooleanField(default=True, verbose_name='Опубликованно')
    bonusactions = models.BooleanField(default=False, verbose_name='Акции')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name='Теги')
    category = models.ForeignKey(PostsCategory, related_name='posts', verbose_name='Категории', on_delete=models.PROTECT)
    sort_id = models.IntegerField(blank=True, verbose_name='Сортировка')
    comments = GenericRelation('comment')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('craft:post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class MenuCategory(models.Model):

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, )
    sort_id = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('craft:product_list_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория Меню'
        verbose_name_plural = 'Категории Меню'
        ordering = ['sort_id']


class Product(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, )
    composition = models.TextField(blank=True, verbose_name='Состав')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Созданно')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменение')
    published = models.BooleanField(default=True, verbose_name='Опубликованно')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    tags = models.ManyToManyField(Tag, related_name='related_product', verbose_name='Теги')
    category = models.ForeignKey(MenuCategory, related_name='related_product', verbose_name='Категории',
                                 on_delete=models.CASCADE,)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    sort_id = models.IntegerField(verbose_name='Сортировка', blank=True)
    in_order = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('craft:product', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('craft:add-to-cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('craft:remove-from-cart', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['-sort_id']
        index_together = (('id', 'slug'),)


class CartProduct(models.Model):

    objects = None
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    ordered = models.BooleanField(default=False)
    # cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE,
    #                          related_name='related_card_products')
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quality = models.IntegerField(default=1)
    # final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f"{self.quality} of {self.product.title} "

    def get_total_price(self):
        return self.quality * self.product.price

    def get_final_price(self):
        return self.get_total_price()

    # def get_absolute_url(self):
    #     return reverse('cartproduct', kwargs={'slug': self.slug})


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct,)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

# class Cart(models.Model):
#     owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
#     products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
#     total_products = models.PositiveIntegerField(default=0)
#     final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
#     in_order = models.BooleanField(default=False)
#     fro_anonymous_user = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.id)
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзины'
#
#
# class Customer(models.Model):
#
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, verbose_name='Номер телефона')
#     address = models.CharField(max_length=255, verbose_name='Адрес')
#
#     def __str__(self):
#         return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


# class Order(models.Model):
#     pass


class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    parent = models.ForeignKey(
            'self',
            verbose_name='Родительский комментарий',
            blank=True,
            null=True,
            related_name='comment_children',
            on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_parent(self):
        if not self.parent:
            return ""
        return self.parent

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'
