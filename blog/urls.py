from django.contrib import admin
from django.urls import path
from blog.views import HomeView, ArticleView, AddPost ,EditPost, DeletePost, AddCategory,DeleteCategory,EditCategory,AdminPanel,DeleteReport
from blog.views import search_view, category_view ,categories_view,top_list_view,DeleteComment,EditComment,ReportView
from functions.decorators import superuser_only,login_only,staff_only



urlpatterns = [

    path('panel-administracyjny',      superuser_only(AdminPanel.as_view()), name="panel-administracyjny"), 

    path('',                           HomeView.as_view() ,name="home"), 
    path('szukaj',                     search_view, name='search'),
    path('kategorie',                  categories_view, name='categories'),
    path('najpopularniejsze-wpisy',    top_list_view,name="top_list"),
    path('kategoria/<str:input_cat>',  category_view, name='category'),
    path('<str:text_to_url>',          ArticleView.as_view(), name="article-view"), 
    

  
    path('usun/komentarz/<slug>',    login_only(DeleteComment.as_view()),name="delete-comment"),
    path('edytuj/komentarz/<slug>',  login_only(EditComment.as_view()),name="edit-comment"),
    path('zglos/komentarz/<slug>',   login_only(ReportView.as_view()),name="report-comment"),


 
    path('dodaj/post',             staff_only(AddPost.as_view()), name='add-post'),
    path('edytuj/post/<slug>',     staff_only(EditPost.as_view()), name='edit-post'),
    path('delete/post/<slug>',     staff_only(DeletePost.as_view()), name='delete-post'),

    path('zglos/komentarz/usun/<pk>', superuser_only(DeleteReport.as_view()),   name="delete-report"),

    path('dodaj/kategorie',             superuser_only(AddCategory.as_view()),    name='add-category'),
    path('edytuj/kategorie/<slug>',     superuser_only(EditCategory.as_view()),   name='edit-category'),
    path('usun/kategorie/<slug>',       superuser_only(DeleteCategory.as_view()), name='delete-category'),
   
]
