from django.urls import path
from shopapp.apis import *

urlpatterns = [
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/review/', ProductReviewAPIView.as_view(), name='product-review'),

    path('catalog/', ProductListAPIView.as_view(), name='catalog'),
    path('products/popular/', PopularListAPIView.as_view(), name='popular'),
    path('products/limited/', LimitedListAPIview.as_view(), name='popular'),
    path('categories/', CategoryListAPIview.as_view(), name='categories'),
    path('sales/', SalesAPIView.as_view(), name='sale'),
    path('banners/', BannersAPIView.as_view(), name='banners'),

    path('orders', OrderListCreateAPIView.as_view(), name='orders'),
    path('order/<int:pk>', OrderAPIView.as_view(), name='order_detail'),

    path('profile', ProfileAPIView.as_view(), name='profile'),
    path('profile/password', ChangePasswordAPIView.as_view(), name='profile-password'),
    path('profile/avatar', ChangeAvatarAPIView.as_view(), name='profile-avatar'),

    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-out', SignOutView.as_view(), name='sign-out'),

    path('tag', TagAPIView.as_view(), name='tag'),

    path('basket', BasketAPIView.as_view(), name='basket'),

    path('payment/<int:pk>', PaymentAPIView.as_view(), name='payment'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='prodduct'),
]


