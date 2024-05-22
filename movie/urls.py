# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('categories/', views.categories, name='categories'),
    path('movie_details/', views.movie_details, name='movie_details'),
    path('search_movie/', views.search_movie, name='search_movie'),  # Thêm URL cho việc tìm kiếm chi tiết phim
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('checkout/', views.checkout, name='checkout'),  # Thêm URL cho checkout
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Thêm path để xử lý yêu cầu loại bỏ mục từ giỏ hàng 
]
