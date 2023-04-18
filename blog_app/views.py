from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DeleteView, ListView
from django.db.models import Q
from django.utils.datetime_safe import datetime
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Books, Category, BookCountViews, Comment
from .forms import LoginForm, RegistrationForm, BookForm, CommentForm


# Create your views here.


class HomeListView(ListView):
    # функция home_view в классе
    model = Books
    context_object_name = 'books'
    template_name = 'pages/index.html'


class UpdateBook(UserPassesTestMixin, UpdateView):
    model = Books
    form_class = BookForm
    template_name = 'pages/post_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class DeleteBook(UserPassesTestMixin, DeleteView):
    model = Books
    success_url = '/'
    template_name = 'pages/book_confirm_delete.html'

    def test_func(self):
        obj = self.get_object()
        return (obj.author == self.request.user) or self.request.user.is_superuser


class UpdateComment(UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'pages/book_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        obj = self.get_object()
        book = Books.objects.get(pk=obj.book.pk)
        form.save()
        return redirect('book_detail', book.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        book = Books.objects.get(pk=obj.book.pk)
        comments = Comment.objects.filter(book=book)
        context['book'] = book
        context['comments'] = comments
        return context

    def test_func(self):
        obj = self.get_object()
        return (obj.author == self.request.user) or self.request.user.is_superuser


class SearchResults(HomeListView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Books.objects.filter(
            Q(title__iregex=query) | Q(description__icontains=query)
        )


def home_view(request):
    books = Books.objects.all()
    context = {
        'books': books
    }
    return render(request, 'pages/index.html', context)


def category_items(request, category_id):
    category = Category.objects.get(pk=category_id)
    books = Books.objects.filter(category=category)
    context = {
        'books': books
    }
    return render(request, 'pages/index.html', context)


def book_detail(request, book_id):
    book = Books.objects.get(pk=book_id)
    comments = book.comments.filter(book=book)

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key
    book_view = BookCountViews()
    book_view.book = book

    if not request.user.is_authenticated:
        book_views = BookCountViews.objects.filter(session_id=session_id, book=book)
        if not book_views.count() and str(session_id) != 'None':
            book_view.session_id = session_id
    else:
        book_views = BookCountViews.objects.filter(user=request.user, book=book)
        if not book_views.count():
            book_view.user = request.user

    if book_view.session_id or book_view.user:
        book_view.save()
        book.views += 1
        book.save()

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.book = book
            form.save()
            return redirect('book_detail', book.pk)
    else:
        form = CommentForm()

    context = {
        'book': book,
        'form': form,
        'comments': comments
    }
    return render(request, 'pages/book_detail.html', context)


def login_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'pages/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'pages/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def add_recipe(request):
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('book_detail', form.pk)
    else:
        form = BookForm()
    context = {
        'form': form
    }
    return render(request, 'pages/post_form.html', context)


def user_books(request, username):
    user = User.objects.get(username=username)
    books = Books.objects.filter(author=user)
    total_views = sum([book.views for book in books])
    total_comments = sum([book.comments.all().count() for book in books])
    days_left = (datetime.now().date() - user.date_joined.date()).days

    context = {
        'username': username,
        'user': user,
        'books': books,
        'total_views': total_views,
        'total_comments': total_comments,
        'total_books': books.count(),
        'days_left': days_left
    }
    return render(request, 'pages/user_books.html', context)


def del_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        book_id = comment.book.pk
        comment.delete()
        return redirect('book_detail', book_id)
    else:
        raise PermissionDenied


# TODO: Изменять статью могут лишь некоторые
