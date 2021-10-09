from django.urls import path
from .views import (Home, Blog, CartView,
                    checkout,
                    Search, PostByTags, PostByCategory,
                    GetPost, MenuByCategory, SingleProduct,
                    add_to_card, remove_form_cart,
                    register, user_login, user_logout,
                    remove_single_item_from_cart, send_reserve_to_telegram,

                    )

# register, user_login, user_logout, send_reserve_to_telegram,

app_name = 'craft'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('menu/', MenuByCategory.as_view(), name='menu'),
    path('cart/', CartView.as_view(), name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('blog/', Blog.as_view(), name='blog'),
    path('search/', Search.as_view(), name="search"),
    path('tag/<str:slug>/', PostByTags.as_view(), name="tag"),
    path('category/<str:slug>/', PostByCategory.as_view(), name="category"),
    path('single_post/<str:slug>/', GetPost.as_view(), name="post"),
    path('single_product/<str:slug>/', SingleProduct.as_view(), name="product"),
    path('add-to-cart/<str:slug>/', add_to_card, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/', remove_form_cart, name='remove-from-cart'),
    path('remove-product-from-cart/<str:slug>/', remove_single_item_from_cart, name='remove-single-product-from-cart'),
    path('register', register, name='register'),
    path('user_login', user_login, name='login'),
    path('user_logout', user_logout, name='logout'),
    path('send_reserve_to_telegram/', send_reserve_to_telegram, name='send_reserve_to_telegram'),
    # path('menu/', product_list, name='product_list'),
    # path('<slug:category_slug>/', product_list, name='product_list_by_category'),
    # # path('add-to-cart/', AddToCardView.as_view(), name='add_to_cart'),
    # path('menu/<str:category_slug>/', product_list, name='product_list_by_category'),
]
# path('create-comment/', create_comment, name='comment_create'),
# path('create-child-comment/', create_child_comment, name='comment_child_create'),
# path('post-comments/', index),
