from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('category/<str:genre>/', views.category_view, name='category_view'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('pay/', views.pay, name='pay'),
    path('user/settings/', views.user_settings, name='user_settings'),
    path('logout/', views.logout_view, name='logout'),
]
