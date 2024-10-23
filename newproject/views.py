import random
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q  # Complex queries work exactly like OR operator. If any of the contition is true the result will be fetched from database.

from myapp.models import Author, Book
from django.db.models import Count, Avg
from django.db import transaction

book_list = [
    {
        'title': 'Peer e Kamil',
        'publish_date': '2023-01-15',
        'price': 1200,
        'status': 'published'
    },
    {
        'title': 'Jannat ki Ser',
        'publish_date': '2024-01-15',
        'price': 1500,
        'status': 'published'
    },
]

def author_book(author_name, book_list):
    try:
        with transaction.atomic():
            author, created = Author.objects.get_or_create(name=author_name)
            
            for book_data in book_list:
                book_exists = Book.objects.filter(title=book_data['title'], author=author)
                if not book_exists:
                    Book.objects.create(
                        title = book_data['title'],
                        publish_date = book_data['publish_date'],
                        price = book_data['price'],
                        author = author,
                        status = book_data['status']
                    )
                else:
                    print("Book with this author already exist")
                    
    except Exception as e:
        print(f"Error: {e}")
        
        
@login_required(login_url="/")
def home(request):
    return render(request, "index.html")

@login_required(login_url="/")
def about(request):
    return render(request, "about.html")

@login_required(login_url="/")
def contact(request):  
    author_book("Furqan", book_list)  
    return render(request, "contact.html")

@login_required(login_url="/")
def service(request):
    return render(request, "service.html")

def roadmap(request): 
    data = {}
    book = Book.objects.filter(Q(price=100) | Q(title='English'))
    
    author_book_count = Author.objects.annotate(num_books = Count('book'))
    average_books = Author.objects.aggregate(average_books_price=Avg('book__price'))
    
    books_of_authors = Book.objects.select_related('author').all()
    authors = Author.objects.prefetch_related('book_set').all()
    
    data = {
        'book':book,
        'author_book_count':author_book_count,
        'average_books': average_books,
        'books_of_authors':books_of_authors,
        'authors':authors,
    }
    
    return render(request, "roadmap.html", data)

def signin(request):
    if request.method == "POST":
        Username = request.POST.get('username')
        Password = request.POST.get('password')
        
        user = authenticate(request, username=Username, password=Password)
        
        if user is not None:
            login(request, user)
            return redirect("Home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("Signin")
        
    return render(request, "signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        email = request.POST.get('email')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        
        
        if username and password and confirm_password and email is not None:
            if password == confirm_password:
                user = User(username=username, email=email, password=password, first_name=f_name, last_name=l_name)
                user.save()
                messages.success(request, "Account Created Successfully")
                return redirect('Home')
            else:
                messages.error(request, "Passwords do not match")
                return redirect('Signup')
        else:
            messages.error(request, "Please fill all the fields")
            return redirect('Signup')
            
    return render(request, "signup.html")

def signout(request):
    logout(request)
    return redirect("Signin")

def generate_otp():
    return random.randint(100000, 999999)

def request_otp_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            otp = generate_otp()
            request.session["otp"] = otp
            request.session["username"] = user.username 
            
            return render(request, "show_otp.html", {'otp': otp})
        except User.DoesNotExist:
            return render(request, "request_otp.html", {'error': "User not found"})
        
    return render(request, "request_otp.html")


def show_otp_view(request):
    session_otp = request.session.get('otp')
    session_username = request.session.get('username')

    if request.method == "POST":
        new_otp = request.POST.get('new_otp')
        password = request.POST.get('password')
        
        if int(new_otp) == session_otp:
            try:
                user = User.objects.get(username=session_username)
                user.set_password(password)
                user.save()
                
                del request.session['otp']
                del request.session['username']
                
                return redirect("Signin")
            
            except User.DoesNotExist:
                messages.error(request, "User not found")
                return redirect("ShowOtp")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("ShowOtp")
    return render(request, "show_otp.html", {'otp':session_otp})

#customer header
def custom_header_test(request):
    custom_header = request.META.get('HTTP_CUSTOM_HEADER', 'Not set')
    return HttpResponse(f"Custom Request Header: {custom_header}")

