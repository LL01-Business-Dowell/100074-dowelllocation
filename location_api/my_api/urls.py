from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from my_api import views

urlpatterns = [
        path('', views.home),
        path('home/', views.api, name='home'),

        path('api/',views.api, name='api'),

    path('continents/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.ContinentList.as_view()),
    path('countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.CountryList.as_view()),
    # path('country/<int:pk>/', views.CountryDetail.as_view()),
    path('country/<slug:query_type>/<slug:query_value>/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.CountryDetail.as_view()),
    path('region/<int:pk>/', views.RegionDetail.as_view()),
    path('region/<slug:query_type>/<str:query_value>/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.RegionDetail.as_view()),
    path('target-function/', views.target_func, name='target-funtion'),
    path('target-func/<slug:collection>/<slug:fields>/<slug:mongoId>/<str:name>/', views.TargetFuntion.as_view(), name='target-func'),
    path('log-in-func/', views.log_in_func, name='log-in'),
    path('logger/', views.LoInFunc.as_view()),
    path('loc-creator/', views.loc_creator, name='loc-creator'),
    path('local-continents/', views.local_continents, name='local-continents'),
    path('local-countries/<int:pk>', views.local_countries, name='local-countries'),
    path('local-regions/<int:pk>', views.local_regions, name='local-regions'),
    path('sync-func/', views.sync_func, name='sync-func'),
    path('rec-tz/', views.rec_tz, name='rec-tz'),

    
    path('display-req-resp/', views.DisplayReqResp.as_view(), name='display-req-resp'),

    path('sync-function/', views.SyncFunc.as_view(), name='sync-function'),
    path('create-loc/', views.CreateFunc.as_view(), name='create-loc'),


]

urlpatterns = format_suffix_patterns(urlpatterns)