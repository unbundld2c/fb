"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp.views import ad_data
from myapp.views import campaign_insights
from myapp.views import account_data
from myapp.views import account
from myapp.f_account import account_matrix
from myapp.f_index import get_all_accounts
from myapp.f_login import get_facebook_access_token
from myapp.f_graph import generate_graph
from myapp.f_campaigns import campaign_insights
from myapp.f_adsets import adset_insights
from myapp.f_ads import ad_insights
from myapp.f_breakdown import breakdown_age, breakdown_gender, breakdown_placement, breakdown_platform
from myapp.s_index import get_shopify_analytics
from myapp.download import download_csv

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('ad-data/', ad_data, name='ad_data'),
    # path('insights/', campaign_insights, name='campaign_insights'),
    # path('account_old/', account_data, name='account_data'),
    path('facebook/', get_all_accounts, name='get_all_accounts'),
    path('facebook/<slug:id>/', account_matrix, name='account_matrix'),
    path('facebook/<slug:id>/campaigns', campaign_insights, name='campaign_insights'),
    path('facebook/<slug:id>/adsets', adset_insights, name='adset_insights'),
    path('facebook/<slug:id>/ads', ad_insights, name='ad_insights'),
    path('facebook/<slug:id>/graph', generate_graph, name='generate_graph'),
    path('facebook/<slug:id>/breakdown-age', breakdown_age, name='breakdown-age'),
    path('facebook/<slug:id>/breakdown-gender', breakdown_gender, name='breakdown-gender'),
    path('facebook/<slug:id>/breakdown-platform', breakdown_platform, name='breakdown_platform'),
    path('facebook/<slug:id>/breakdown-placement', breakdown_placement, name='breakdown-placement'),
    path('shopify/', get_shopify_analytics, name='get_shopify_analytics'),
    path('auth/', get_facebook_access_token, name='auth'),
    path('download/', download_csv, name='download_csv'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)