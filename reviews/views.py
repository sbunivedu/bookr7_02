from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from .models import Book, Contributor
from .utils import average_rating

def index(request):
    return render(request, "base.html")

def book_search(request):
    print(request.GET) # for debugging

    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()

    print(f"form.is_valid()=>{form.is_valid()}")
    print(f"form.cleaned_data['search']=>{form.cleaned_data['search']}")

    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        books = Book.objects.filter(title__icontains=search)

    return render(
        request,
        "reviews/search-results.html",
        {"form": form, "search_text": search_text, "books": books},
    )

def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book,
                          'book_rating': book_rating,
                          'number_of_reviews': number_of_reviews})

    context = {
        'book_list': book_list
    }
    return render(request, 'reviews/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }
    return render(request, "reviews/book_detail.html", context)
