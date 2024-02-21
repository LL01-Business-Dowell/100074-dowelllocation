from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from my_api import views
from my_api import loc_recs_view
from my_api import locs_rec_view_2
from my_api import locs_rec_view_3
from my_api import health_check_views
urlpatterns = [
        path('', views.api),
        path('home/', views.api, name='home'),

        path('api/',views.api, name='api'),
    path('get-coords/', views.GetCoords.as_view()),
path('get-coords-v2/', views.GetCoords2.as_view()),
    path('continents/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.ContinentList.as_view()),
    path('countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.CountryList.as_view()),
    # path('countries/<slug:sessionId>/<slug:projectCode>/', views.CountryList.as_view()),
    path('regions/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.RegionList.as_view()),
    path('regions/', views.RegionList2.as_view()),
    # path('country/<int:pk>/', views.CountryDetail.as_view()),
    path('country/<slug:query_type>/<str:query_value>/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.CountryDetail.as_view()),
    path('region/<int:pk>/', views.RegionDetail.as_view()),
    path('region/<slug:query_type>/<str:query_value>/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.RegionDetail.as_view()),
    # path('region/<slug:query_type>/<str:query_value>/<slug:sessionId>/<slug:projectCode>/', views.RegionDetail.as_view()),
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
    path('gen-loc-json/', views.gen_loc_json, name='gen-loc-json'),

    path('create-continent/', loc_recs_view.create_continent, name='create_continent'),
    path('create-country/', loc_recs_view.create_country, name='create_country'),
    path('create-region/', loc_recs_view.create_region, name='create_region'),
    path('update/<int:pk>', loc_recs_view.update_region, name='update-region'),
    path('create-sub-region/', loc_recs_view.create_sub_region, name='create_sub_region'),
    path('my-form-test/', loc_recs_view.my_form_test, name='my-form-test'),
    path('get-countries-v3/', locs_rec_view_2.GetCountries3.as_view(), name='get-countries-v3'),
    path('get-coords-v3/', locs_rec_view_2.GetCoords3.as_view(), name='get-coords-v3'),
    path('get-coords-v4/', locs_rec_view_2.GetCoords4.as_view(), name='get-coords-v4'),
    path('display-req-resp/', views.DisplayReqResp.as_view(), name='display-req-resp'),

    path('sync-function/', views.SyncFunc.as_view(), name='sync-function'),
    path('create-loc/', views.CreateFunc.as_view(), name='create-loc'),
    path('insert-mylocs/', views.insert_mylocs, name='insert-mylocs'),

    ##Exile urls
    path('get-locs/', locs_rec_view_3.GetLocations.as_view()),
    path('create-profile/', locs_rec_view_3.CreateUserProfile.as_view()),
    path('create-loc-group/', locs_rec_view_3.CreateLocGroup.as_view()),
    path('create-location/', locs_rec_view_3.CreateLocation.as_view()),
    path('update-loc-group/', locs_rec_view_3.UpdateLocGroup.as_view()),
    path('update-location/', locs_rec_view_3.UpdateLocation.as_view()),
    path('delete-user-locs/', locs_rec_view_3.DeleteUserProfile.as_view()),
    path('delete-loc-group/', locs_rec_view_3.DeleteLocGroup.as_view()),
    path('delete-loc/', locs_rec_view_3.DeleteLocation.as_view()),
    path('sync-groups/', locs_rec_view_3.SyncGroups.as_view()),
    ##health_check
    path('health-check/', health_check_views.HealthCheck.as_view(), name='health-check'),





]

urlpatterns = format_suffix_patterns(urlpatterns)