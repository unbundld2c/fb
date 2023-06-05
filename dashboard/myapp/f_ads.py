from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.conf import settings
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from dotenv import load_dotenv
import os

load_dotenv()

today = date.today() - timedelta(days=1)
yesterday = date.today() - timedelta(days=1)
last_3_days = date.today() - timedelta(days=3)
last_7_days = date.today() - timedelta(days=7)
last_30_days = date.today() - timedelta(days=30)

fields = [
    'campaign_name',
    'adset_name',
    'ad_name',
    'objective',
    'impressions',
    'reach',
    'spend',
    'frequency',
    'purchase_roas',
    'cost_per_inline_link_click',
    'outbound_clicks_ctr',
    'cpm',
    'cpc',
    'ctr',
    'actions',
]

def ad_insights(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))
    
    yesterday_ad_insights = account.get_insights(
        fields=fields,
        params={
            'time_range': {
                'since': str(yesterday),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    
    yesterday_ads = []
    for insight in yesterday_ad_insights:
        data = {}
        data['cname'] = insight.get('campaign_name', '')
        data['aname'] = insight.get('adset_name', '')
        data['name'] = insight.get('ad_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['purchase_roas'] = insight.get('purchase_roas', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['outbound_clicks_ctr'] = insight.get('outbound_clicks_ctr', [])
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        yesterday_ads.append(data)

    last_3_days_ad_insights = account.get_insights(
        fields=fields,
        params={
            'time_range': {
                'since': str(last_3_days),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    
    last_3_days_ads = []
    for insight in last_3_days_ad_insights:
        data = {}
        data['cname'] = insight.get('campaign_name', '')
        data['aname'] = insight.get('adset_name', '')
        data['name'] = insight.get('ad_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['purchase_roas'] = insight.get('purchase_roas', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['outbound_clicks_ctr'] = insight.get('outbound_clicks_ctr', [])
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        last_3_days_ads.append(data)
    
    last_7_days_ad_insights = account.get_insights(
        fields=fields,
        params={
            'time_range': {
                'since': str(last_7_days),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    
    last_7_days_ads = []
    for insight in last_7_days_ad_insights:
        data = {}
        data['cname'] = insight.get('campaign_name', '')
        data['aname'] = insight.get('adset_name', '')
        data['name'] = insight.get('ad_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['purchase_roas'] = insight.get('purchase_roas', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['outbound_clicks_ctr'] = insight.get('outbound_clicks_ctr', [])
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        last_7_days_ads.append(data)
    
    last_30_days_ad_insights = account.get_insights(
        fields=fields,
        params={
            'time_range': {
                'since': str(last_30_days),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    
    last_30_days_ads = []
    for insight in last_30_days_ad_insights:
        data = {}
        data['cname'] = insight.get('campaign_name', '')
        data['aname'] = insight.get('adset_name', '')
        data['name'] = insight.get('ad_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['purchase_roas'] = insight.get('purchase_roas', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['outbound_clicks_ctr'] = insight.get('outbound_clicks_ctr', [])
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        last_30_days_ads.append(data)

    # print(yesterday_ads)
    return render(request, 'myapp/facebook/ads.html', {
        'yesterday_ads': yesterday_ads,
        'last_3_days_ads': last_3_days_ads,
        'last_7_days_ads': last_7_days_ads,
        'last_30_days_ads': last_30_days_ads,
    })