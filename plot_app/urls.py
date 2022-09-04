from django.conf.urls import url
from django.contrib import admin
from plot_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index ),
    path('home', views.HomeView.as_view()),
    # path('test-api', views.get_data),
    path('api', views.ChartData.as_view()),
    path('repos', views.RepoData.as_view()),
]
