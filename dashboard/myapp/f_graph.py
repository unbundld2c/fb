from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import render
from datetime import datetime, timedelta, date
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from dotenv import load_dotenv
import os
load_dotenv()

@cache_page(60*600)
def generate_graph(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))

    fields = [
       'account_name',
       'account_id',
    ]

    labels_cache_key = f'labels_{str(id)}'
    labels = cache.get(labels_cache_key)
    cpm_data_cache_key = f'cpm_data_{str(id)}'
    cpm_data = cache.get(cpm_data_cache_key)
    cpc_data_cache_key = f'cpc_data_{str(id)}'
    cpc_data = cache.get(cpc_data_cache_key)
    cpilc_data_cache_key = f'cpilc_data_{str(id)}'
    cpilc_data = cache.get(cpilc_data_cache_key)
    occ_data_cache_key = f'occ_data_{str(id)}'
    occ_data = cache.get(occ_data_cache_key)

    if labels is None or cpm_data is None or cpc_data is None or cpilc_data is None or occ_data is None:
        labels = []
        cpm_data = []
        cpc_data = []
        cpilc_data = []
        occ_data = []

        for i in range(30):
            chart_date_end = date.today() - timedelta(days=i)
            chart_date_start = chart_date_end - timedelta(days=1)
            date_str = chart_date_end.strftime('%m/%d')
            labels.insert(0, date_str)
            chart_insights = account.get_insights(
                fields={
                    'cpm',
                    'cpc',
                    'cost_per_inline_link_click',
                    'outbound_clicks_ctr'
                },
                params={
                    'time_range': {
                        'since': str(chart_date_start),
                        'until': str(chart_date_end),
                    },
                    'level': 'account',
                }
            )
            metrics = chart_insights[0]
            cpm_data.insert(0, metrics.get('cpm', 0))
            cpc_data.insert(0, metrics.get('cpc', 0))
            cpilc_data.insert(0, metrics.get('cost_per_inline_link_click', 0))
            occ_data.insert(0, metrics.get('outbound_clicks_ctr', 0)[0]["value"])
        cache.set(labels_cache_key, labels)
        cache.set(cpm_data_cache_key, cpm_data)
        cache.set(cpc_data_cache_key, cpc_data)
        cache.set(cpilc_data_cache_key, cpilc_data)
        cache.set(occ_data_cache_key, occ_data)

    # print(id)

    return render(request, 'myapp/facebook/graph.html',{
        'labels' : labels,
        'cpm_data' : cpm_data,
        'cpc_data' : cpc_data,
        'cpilc_data' : cpilc_data,
        'occ_data' : occ_data,
    })