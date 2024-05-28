from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Movie, Cart, CartItem
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.contrib import messages


# Load movie data into a DataFrame
movies = Movie.objects.all().values('id', 'title', 'overview', 'poster_path', 'runtime', 'release_date', 'genres', 'movie_id', 'price')
df2 = pd.DataFrame(list(movies))

# Debugging: Print DataFrame columns and first few rows
print("DataFrame Columns:", df2.columns)
print("DataFrame Head:", df2.head())

# Check if 'overview' column is present in the DataFrame
if 'overview' in df2.columns:
    # Create TF-IDF matrix and cosine similarity matrix for recommendations
    tfidf = TfidfVectorizer(stop_words='english')
    df2['overview'] = df2['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df2['overview'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()
else:
    print("Error: 'overview' column is missing in the DataFrame")

def get_recommendations(title, cosine_sim=None):
    if cosine_sim is None:
        return []
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df2['title'].iloc[movie_indices]

@login_required
def home(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)  # Show 10 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movie_list1.html', {'page_obj': page_obj})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    data = {
        'title': movie.title,
        'overview': movie.overview,
        'genres': movie.genres,
        'release_date': movie.release_date,
        'runtime': movie.runtime,
        'poster_path': movie.get_poster_url(),  # Ensure correct poster URL
        'price': movie.price,  # Ensure this line is included
    }
    recommended_movies = get_recommendations(movie.title, cosine_sim)
    print("Recommended movies for {}: {}".format(movie.title, recommended_movies))
    return JsonResponse(data)

def category_view(request, genre):
    movies = Movie.objects.filter(genres__icontains=genre)
    genres = Movie.objects.values_list('genres', flat=True).distinct()
    return render(request, 'movie_list1.html', {'movies': movies, 'genres': genres, 'selected_genre': genre})

def login_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login1.html', {'error': 'Invalid username or password'})
        elif 'signup' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            if User.objects.filter(username=username).exists():
                return render(request, 'login1.html', {'error': 'Username already exists'})
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'login1.html')

@login_required
def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the movie is already in the cart
    if CartItem.objects.filter(cart=cart, movie=movie).exists():
        messages.info(request, 'This movie is already in your cart.')
        return redirect('view_cart')

    # If not, add the movie to the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.movie.price * item.quantity for item in cart_items)  # Assuming `price` is a field in Movie
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, movie_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, movie_id=movie_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def pay(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_amount = sum(item.movie.price * item.quantity for item in cart_items)  # Assuming `price` is a field in Movie
    return render(request, 'pay.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required
def user_settings(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        email = request.POST.get('email', user.email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return render(request, 'user_settings.html', {'user': user, 'success': True})
    return render(request, 'user_settings.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('login')
