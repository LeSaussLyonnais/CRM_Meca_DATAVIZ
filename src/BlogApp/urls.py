from django.urls import path, include
#from django.conf.urls import url
from .views import index, article, WeatherView

urlpatterns = [
    path('', index, name="blog-index"),
    path('article<str:num_article>/', article, name="blog-article"),
    path('React', WeatherView.as_view(), name="WeatherReactView")
]