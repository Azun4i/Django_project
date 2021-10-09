from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect


from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic import View
from .forms import UserRegisterForm, UserloginForm, ReserveForm
from django.contrib.auth import login, logout
from cart.forms import CartAddProductForm
# from .utils import create_comments_tree

from .models import *
# from craft.telegram.bot_utils import send_massages
# from .forms import CommentForm


class Home(ListView):
    model = Post
    template_name = 'craft/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CRAFT'
        return context


class Blog(ListView):
    model = Post
    template_name = 'craft/blog.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(published_at=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BLOG'
        return context


class Search(ListView):
    template_name = 'craft/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f's={self.request.GET.get("s")}&'
        return context


class PostByCategory(ListView):
    model = Post
    template_name = "craft/post_category.html"
    context_object_name = 'cats'
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Посты по категории'
        return context


class PostByTags(ListView):
    model = Post
    template_name = 'craft/post_tags.html'
    context_object_name = 'tags'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегам: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetPost(DetailView):
    # single post
    model = Post
    template_name = 'craft/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class MenuByCategory(ListView):
    model = MenuCategory
    template_name = 'craft/menu.html'
    context_object_name = 'menus'

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Menu'
        context['categories'] = MenuCategory.objects.all()
        return context


class SingleProduct(DetailView):
    model = Product
    template_name = 'craft/single_product.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Product.objects.get(slug=self.kwargs['slug'])
        return context
# context_object_name = 'cart_list'


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'craft/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "У вас нет покупок")
            return redirect('craft:home')


@login_required
def add_to_card(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = CartProduct.objects.get_or_create(product=product,
                                                            user=request.user,
                                                            ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # проверяем есть ли в корзине продукт из заказа
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quality += 1
            order_item.save()
            messages.info(request, "Колличество было изменнено!")
            return redirect("craft:cart")
        else:
            messages.info(request, "Добавлен в вашу корзину!")
            order.products.add(order_item)
            return redirect("craft:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_item)
        messages.info(request, "Добавлен в вашу корзину!")
        return redirect("craft:menu")


@login_required
def remove_form_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # проверяем есть ли в корзине продукт из заказа
        if order.products.filter(product__slug=product.slug).exists():
            order_item = CartProduct.objects.filter(product=product,
                                                    user=request.user,
                                                    ordered=False)[0]
            order.products.remove(order_item)
            messages.info(request, "Удален с вашей корзины!")
            return redirect("craft:cart")
        else:
            messages.info(request, "Итема нет в вашей корзине!")
            return redirect("craft:cart")
    else:
        messages.info(request, "У вас нет активных корзин!")
        return redirect("craft:menu")


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # проверяем есть ли в корзине продукт из заказа
        if order.products.filter(product__slug=product.slug).exists():
            order_item = CartProduct.objects.filter(product=product,
                                                    user=request.user,
                                                    ordered=False)[0]
            if order_item.quality > 1:
                order_item.quality -= 1
                order_item.save()
            else:
                order.products.remove(order_item)
            messages.info(request, "Колличество было изменено!")
            return redirect("craft:cart")
        else:
            messages.info(request, "Итема нет в вашей корзине!")
            return redirect("craft:cart")
    else:
        messages.info(request, "У вас нет активных корзин!")
        return redirect("craft:menu")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались.")
            return redirect('craft:home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'craft/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserloginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('craft:home')
    else:
        form = UserloginForm()
    return render(request, 'craft/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('craft:login')


def checkout(request):
    return render(request, "craft/checkout.html")


def send_reserve_to_telegram(request):
    if request.method == 'POST':
        form = ReserveForm(request.POST)
        text = f'Имя: {form.data["username"]}' \
               f'\nНомер телефона: {form.data["phone_number"]}' \
               f'\nДата: {form.data["date"]}' \
               f'\nВремя резерва: {form.data["time"]}' \
               f'\nПримечание: {form.data["massages"]}'
        # send_massages(text)
        # if send_massages:
        #     messages.info(request, 'Запрос о резерве отправлен.')
        # else:
        #     messages.error(request, 'Ошибка отправки.')
        # return redirect('craft:home')
    else:
        form = ReserveForm()
    return render(request, 'craft/index.html', {'form': form})
#

# class AddToCardView(View):
#
#     def get_queryset(self):
#         return Product.objects.get(slug=self.kwargs['slug'])
#
#     # def get_context_data(self, *, object_list=None, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['title'] = 'Записи по тегам: '
#     #     context['title'] = Product.objects.get(slug=self.kwargs['slug'])
#     #     return context
#
#     def get(self, request, *args, **kwargs):
#         ct_models, product_slug = Product.objects.filter(slug=self.kwargs['slug'])
#         print(ct_models, product_slug)
#         customer = Customer.objects.get(user=request.user)
#         cart = Cart.objects.get(owner=customer, in_order=False)
#         category = MenuCategory.objects.get(model=ct_models)
#         product = category.model_class().objects.get(slug=product_slug)
#         cart_product = CartProduct.objects.create(
#             user=cart.owner, cart=cart, content_object=product, final_price=product.price
#         )
#         cart.products.add(cart_product)
#         return HttpResponseRedirect('/cart/')


# def index(request):
#     comments = Post.objects.first().comments.all()
#     result = create_comments_tree(comments)
#     comment_form = CommentForm(request.POST or None)
#     return render(request, 'craft/test.html', {'comments': result, 'comment_form': comment_form})


# def create_comment(request):
#     comment_form = CommentForm(request.POST or None)
#     if comment_form.is_valid():
#         new_comment = comment_form.save(commit=False)
#         new_comment.user = request.user
#         new_comment.text = comment_form.cleaned_data['text']
#         new_comment.content_type = ContentType.objects.get(model='post')
#         new_comment.object_id = 4
#         new_comment.parent = None
#         new_comment.is_child = False
#         new_comment.save()
#     return HttpResponseRedirect('craft:/post-comments')


# @transaction.atomic
# def create_child_comment(request):
#     user_name = request.POST.get('user')
#     current_id = request.POST.get('id')
#     text = request.POST.get('text')
#     user = User.objects.get(username=user_name)
#     content_type = ContentType.objects.get(model='post')
#     parent = Comment.objects.get(id=int(current_id))
#     is_child = False if not parent else True
#     Comment.objects.create(
#         user=user, text=text, content_type=content_type, object_id=4,
#         parent=parent, is_child=is_child,
#     )
#     comments_ = Post.objects.first().comments.all()
#     comments_list = create_comments_tree(comments_)
#     return render(request, 'craft/test.html', {'comments': comments_list})



# def product_list(request, category_slug=None):
#     category = None
#     categories = MenuCategory.objects.all()
#     products = Product.objects.filter(published=True)
#     if category_slug:
#         category = get_object_or_404(MenuCategory, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request, 'craft/menu.html',
#                   {
#                        "category": category,
#                        "categories": categories,
#                        "products": products, })  #'cart_product_form': cart_product_form
#
#
# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, published=True)
#     return render(request, 'cart/detail.html', {'product': product})


