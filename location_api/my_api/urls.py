from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from my_api import views

urlpatterns = [
    path('countries/', views.CountryList.as_view()),
    # path('country/<int:pk>/', views.CountryDetail.as_view()),
    path('country/<slug:query_type>/<slug:query_value>/', views.CountryDetail.as_view()),
    path('region/<int:pk>/', views.RegionDetail.as_view()),
     path('region/<slug:query_type>/<slug:query_value>/', views.RegionDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)