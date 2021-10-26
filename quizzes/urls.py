from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('questions/<slug:slug>/', views.question, name='question'),
    path('check/', views.check, name='check'),
    path('user_account/', views.ResultListView.as_view(), name='user_account'),

]
