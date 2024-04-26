from django.urls import path, include
#from django.conf.urls import url
from .views import index, ordo, article, WeatherView, charge

urlpatterns = [
    path('', index, name="blog-index"),
    path('ordo', ordo, name="blog-ordo"),
    path('charge/', charge, name="charge"),
    path('article<str:num_article>/', article, name="blog-article"),
    path('React', WeatherView.as_view(), name="WeatherReactView")
]