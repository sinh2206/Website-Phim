# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Movie

def index(request):
    popular_movies = Movie.objects.filter(category='popular')[:4]
    new_movies = Movie.objects.filter(category='new')[:4]
    return render(request, 'index.html', {
        'popular_movies': popular_movies,
        'new_movies': new_movies,
    })


def cart(request):
    # Giả sử bạn đã có logic để lấy các mặt hàng trong giỏ hàng và tính tổng giá
    cart_items = []  # Thay thế bằng logic thực tế
    total_price = 0  # Thay thế bằng logic thực tế
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def categories(request):
    years = range(2000, 2025)
    ratings = range(1, 6)  # Thêm ratings từ 1 đến 5
    
    # Lấy danh sách phim từ cơ sở dữ liệu
    movies = Movie.objects.all()  # Đây là một ví dụ, bạn có thể điều chỉnh truy vấn theo yêu cầu của mình
    
    return render(request, 'categories.html', {'years': years, 'ratings': ratings, 'movies': movies})



def movie_details(request):
    return render(request, 'movie_details.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def search_movie(request):
    if request.method == 'GET':
        movie_id = request.GET.get('movie_id')
        movie_title = request.GET.get('movie_title')
        
        if movie_id:
            movie = Movie.objects.filter(id=movie_id).first()
        elif movie_title:
            movie = Movie.objects.filter(title__icontains=movie_title).first()
        else:
            movie = None
        
        if movie:
            return render(request, 'movie_details.html', {'movie': movie})
        else:
            return render(request, 'movie_details.html', {'error_message': 'Movie not found'})

def checkout(request):
    return render(request, 'checkout.html')  # Thêm view checkout

def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart')
