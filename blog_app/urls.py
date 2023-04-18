from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    # path('', views.home_view, name='home'),
    path('categories/<int:category_id>/', views.category_items, name='category_items'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/registrations/', views.registration_view, name='registration'),
    path('accounts/logout/', views.user_logout, name='logout'),

    path('create/', views.add_recipe, name='create'),
    path('update/<int:pk>/', views.UpdateBook.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteBook.as_view(), name='delete'),

    path('search/', views.SearchResults.as_view(), name='search'),
    path('authors/<str:username>/', views.user_books, name='user_books'),
    path('comments/<int:comment_id>/delete/', views.del_comment, name='del_comment'),
    path('comments/<int:pk>/edit/', views.UpdateComment.as_view(), name='edit_comment')
]
