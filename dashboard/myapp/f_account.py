from django.views.decorators.cache import cache_page
from django.core.cache import cache
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.conf import settings
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from dotenv import load_dotenv
import os

load_dotenv()

def calculate_delta(num1, num2):
    if num2 == 0:
        return 0
    else:
        result = round((((num1-num2)/num2)*100),2)
        return result

@cache_page(60*60)
def account_matrix(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))

    fields = [
       'account_name',
       'account_id',
       'spend',
       'cpm',
       'impressions',
       'actions',
       'reach',
       'purchase_roas',
       'frequency',
       'cpc',
       'cost_per_inline_link_click',
       'ctr',
       'outbound_clicks_ctr',
    ]

    today = date.today() - timedelta(days=1)
    yesterday = date.today() - timedelta(days=1)
    last_3_days = date.today() - timedelta(days=3)
    last_7_days = date.today() - timedelta(days=7)
    last_30_days = date.today() - timedelta(days=30)

    yesterday_delta = date.today() - timedelta(days=2)
    last_3_days_delta = date.today() - timedelta(days=6)
    last_7_days_delta = date.today() - timedelta(days=14)
    last_30_days_delta = date.today() - timedelta(days=60)



    # yesterday cacheing

    yesterday_cache_key = f'yesterday_result_{str(id)}'
    yesterday_delta_cache_key = f'yesterday_delta_result_{str(id)}'
    yesterday_result = cache.get(yesterday_cache_key)
    yesterday_delta_result = cache.get(yesterday_delta_cache_key)

    if yesterday_result is None:
        yesterday_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday),
                    'until': str(today),
                },
                'level': 'account',
            }
        )
        yesterday_data = yesterday_insights[0]
        yesterday_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday_delta),
                    'until': str(yesterday_delta),
                },
                'level': 'account',
            }
        )
        yesterday_delta_data = yesterday_delta_insights[0]
        yesterday_result = {
            'account_name': yesterday_data.get('account_name',''),
            'account_id': yesterday_data.get('account_id',''),
            'spend': round(float(yesterday_data.get('spend', 0)),3),
            'cpm': round(float(yesterday_data.get('cpm', 0)),3),
            'impressions': yesterday_data.get('impressions', 0),
            'actions': yesterday_data.get('actions', 0),
            'reach': yesterday_data.get('reach', 0),
            'frequency': round(float(yesterday_data.get('frequency', 0)),3),
            'cpc': round(float(yesterday_data.get('cpc', 0)),3),
            'cost_per_inline_link_click': round(float(yesterday_data.get('cost_per_inline_link_click', 0)),3),
            'ctr': round(float(yesterday_data.get('ctr', 0)),3),
        }
        if yesterday_data.get('purchase_roas', 0) == 0:
            yesterday_result['purchase_roas'] = 0
        else:
            yesterday_result['purchase_roas'] = round(float(yesterday_data.get('purchase_roas')[0]['value']),3) 
        
        if yesterday_data.get('outbound_clicks_ctr', 0) == 0:
            yesterday_result['outbound_clicks_ctr'] = 0
        else:
            yesterday_result['outbound_clicks_ctr'] = round(float(yesterday_data.get('outbound_clicks_ctr')[0]['value']),3) 

        for action in yesterday_result['actions']:
            if action['action_type'] == 'purchase':
                yesterday_result['result'] = action['value']
                break

        
        yesterday_delta_result = {
            'spend': calculate_delta(float(yesterday_data.get('spend', 0)) , float(yesterday_delta_data.get('spend', 0))),
            'cpm': calculate_delta(float(yesterday_data.get('cpm', 0)) , float(yesterday_delta_data.get('cpm', 0))),
            'impressions': calculate_delta(int(yesterday_data.get('impressions', 0)), int(yesterday_delta_data.get('impressions', 0))),
            'reach': calculate_delta(int(yesterday_data.get('reach', 0)), int(yesterday_delta_data.get('reach', 0))),
            'frequency': calculate_delta(float(yesterday_data.get('frequency', 0)), float(yesterday_delta_data.get('frequency', 0))),
            'cpc': calculate_delta(float(yesterday_data.get('cpc', 0)), float(yesterday_delta_data.get('cpc', 0))),
            'cost_per_inline_link_click': calculate_delta(float(yesterday_data.get('cost_per_inline_link_click', 0)), float(yesterday_delta_data.get('cost_per_inline_link_click', 0))),
            'ctr': calculate_delta(float(yesterday_data.get('ctr', 0)), float(yesterday_delta_data.get('ctr', 0))),
            'actions': yesterday_delta_data.get('actions', 0),
        }
        if yesterday_delta_data.get('purchase_roas', 0) == 0:
            yesterday_delta_data['purchase_roas'] = 0
        else:
            yesterday_delta_result['purchase_roas'] = calculate_delta(float(yesterday_data.get('purchase_roas', 0)[0]['value']), float(yesterday_delta_data.get('purchase_roas', 0)[0]['value'])) 
        
        if yesterday_delta_data.get('outbound_clicks_ctr', 0) == 0:
            yesterday_delta_data['outbound_clicks_ctr'] = 0
        else:
            yesterday_delta_result['outbound_clicks_ctr'] = calculate_delta(float(yesterday_data.get('outbound_clicks_ctr', 0)[0]['value']), float(yesterday_delta_data.get('outbound_clicks_ctr', 0)[0]['value'])) 

        for action in yesterday_delta_result['actions']:
            if action['action_type'] == 'purchase':
                yesterday_delta_result['result'] = int(yesterday_result['result']) - int(action['value'])
                break

        cache.set(yesterday_cache_key, yesterday_result)
        cache.set(yesterday_delta_cache_key, yesterday_delta_result)

    # last 3 days cacheing

    last_3_days_cache_key = f'last_3_days_result_{str(id)}'
    last_3_days_delta_cache_key = f'last_3_days_delta_result_{str(id)}'
    last_3_days_result = cache.get(last_3_days_cache_key)
    last_3_days_delta_result = cache.get(last_3_days_delta_cache_key)

    if last_3_days_result is None:
        last_3_days_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days),
                    'until': str(today),
                },
                'level': 'account',
            }
        )
        last_3_days_data = last_3_days_insights[0]
        last_3_days_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days_delta),
                    'until': str(last_3_days - timedelta(days=1)),
                },
                'level': 'account',
            }
        )
        last_3_days_delta_data = last_3_days_delta_insights[0]
        last_3_days_result = {
            'spend': round(float(last_3_days_data.get('spend', 0)),3),
            'cpm': round(float(last_3_days_data.get('cpm', 0)),3),
            'impressions': last_3_days_data.get('impressions', 0),
            'actions': last_3_days_data.get('actions', 0),
            'reach': last_3_days_data.get('reach', 0),
            'frequency': round(float(last_3_days_data.get('frequency', 0)),3),
            'cpc': round(float(last_3_days_data.get('cpc', 0)),3),
            'cost_per_inline_link_click': round(float(last_3_days_data.get('cost_per_inline_link_click', 0)),3),
            'ctr': round(float(last_3_days_data.get('ctr', 0)),3),
        }
        if last_3_days_data.get('purchase_roas', 0) == 0:
            last_3_days_result['purchase_roas'] = 0
        else:
            last_3_days_result['purchase_roas'] = round(float(last_3_days_data.get('purchase_roas')[0]['value']),3) 
        if last_3_days_data.get('outbound_clicks_ctr', 0) == 0:
            last_3_days_result['outbound_clicks_ctr'] = 0
        else:
            last_3_days_result['outbound_clicks_ctr'] = round(float(last_3_days_data.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in last_3_days_result['actions']:
            if action['action_type'] == 'purchase':
                last_3_days_result['result'] = action['value']
                break
        last_3_days_delta_result = {
            'spend': calculate_delta(float(last_3_days_data.get('spend', 0)) , float(last_3_days_delta_data.get('spend', 0))),
            'cpm': calculate_delta(float(last_3_days_data.get('cpm', 0)) , float(last_3_days_delta_data.get('cpm', 0))),
            'impressions': calculate_delta(int(last_3_days_data.get('impressions', 0)), int(last_3_days_delta_data.get('impressions', 0))),
            'reach': calculate_delta(int(last_3_days_data.get('reach', 0)), int(last_3_days_delta_data.get('reach', 0))),
            'frequency': calculate_delta(float(last_3_days_data.get('frequency', 0)), float(last_3_days_delta_data.get('frequency', 0))),
            'cpc': calculate_delta(float(last_3_days_data.get('cpc', 0)), float(last_3_days_delta_data.get('cpc', 0))),
            'cost_per_inline_link_click': calculate_delta(float(last_3_days_data.get('cost_per_inline_link_click', 0)), float(last_3_days_delta_data.get('cost_per_inline_link_click', 0))),
            'ctr': calculate_delta(float(last_3_days_data.get('ctr', 0)), float(last_3_days_delta_data.get('ctr', 0))),
            'actions': last_3_days_delta_data.get('actions', 0),
        }
        if last_3_days_delta_data.get('purchase_roas', 0) == 0:
            last_3_days_delta_data['purchase_roas'] = 0
        else:
            last_3_days_delta_result['purchase_roas'] = calculate_delta(float(last_3_days_data.get('purchase_roas', 0)[0]['value']), float(last_3_days_delta_data.get('purchase_roas', 0)[0]['value'])) 
        if last_3_days_delta_data.get('outbound_clicks_ctr', 0) == 0:
            last_3_days_delta_data['outbound_clicks_ctr'] = 0
        else:
            last_3_days_delta_result['outbound_clicks_ctr'] = calculate_delta(float(last_3_days_data.get('outbound_clicks_ctr', 0)[0]['value']), float(last_3_days_delta_data.get('outbound_clicks_ctr', 0)[0]['value'])) 
        for action in last_3_days_delta_result['actions']:
            if action['action_type'] == 'purchase':
                last_3_days_delta_result['result'] = int(last_3_days_result['result']) - int(action['value'])
                break
        
        cache.set(last_3_days_cache_key, last_3_days_result)
        cache.set(last_3_days_delta_cache_key, last_3_days_delta_result)

    
    # last 7 days cacheing

    last_7_days_cache_key = f'last_7_days_result_{str(id)}'
    last_7_days_delta_cache_key = f'last_7_days_delta_result_{str(id)}'
    last_7_days_result = cache.get(last_7_days_cache_key)
    last_7_days_delta_result = cache.get(last_7_days_delta_cache_key)

    if last_7_days_result is None:
        last_7_days_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days),
                    'until': str(today),
                },
                'level': 'account',
            }
        )
        last_7_days_data = last_7_days_insights[0]
        last_7_days_result = {
            'spend': round(float(last_7_days_data.get('spend', 0)),3),
            'cpm': round(float(last_7_days_data.get('cpm', 0)),3),
            'impressions': last_7_days_data.get('impressions', 0),
            'actions': last_7_days_data.get('actions', 0),
            'reach': last_7_days_data.get('reach', 0),
            'frequency': round(float(last_7_days_data.get('frequency', 0)),3),
            'cpc': round(float(last_7_days_data.get('cpc', 0)),3),
            'cost_per_inline_link_click': round(float(last_7_days_data.get('cost_per_inline_link_click', 0)),3),
            'ctr': round(float(last_7_days_data.get('ctr', 0)),3),
        }
        if last_7_days_data.get('purchase_roas', 0) == 0:
            last_7_days_result['purchase_roas'] = 0
        else:
            last_7_days_result['purchase_roas'] = round(float(last_7_days_data.get('purchase_roas')[0]['value']),3) 
        if last_7_days_data.get('outbound_clicks_ctr', 0) == 0:
            last_7_days_result['outbound_clicks_ctr'] = 0
        else:
            last_7_days_result['outbound_clicks_ctr'] = round(float(last_7_days_data.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in last_7_days_result['actions']:
            if action['action_type'] == 'purchase':
                last_7_days_result['result'] = action['value']
                break
        last_7_days_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days_delta),
                    'until': str(last_7_days - timedelta(days=1)),
                },
                'level': 'account',
            }
        )
        last_7_days_delta_data = last_7_days_delta_insights[0]
        last_7_days_delta_result = {
            'spend': calculate_delta(float(last_7_days_data.get('spend', 0)) , float(last_7_days_delta_data.get('spend', 0))),
            'cpm': calculate_delta(float(last_7_days_data.get('cpm', 0)) , float(last_7_days_delta_data.get('cpm', 0))),
            'impressions': calculate_delta(int(last_7_days_data.get('impressions', 0)), int(last_7_days_delta_data.get('impressions', 0))),
            'reach': calculate_delta(int(last_7_days_data.get('reach', 0)), int(last_7_days_delta_data.get('reach', 0))),
            'frequency': calculate_delta(float(last_7_days_data.get('frequency', 0)), float(last_7_days_delta_data.get('frequency', 0))),
            'cpc': calculate_delta(float(last_7_days_data.get('cpc', 0)), float(last_7_days_delta_data.get('cpc', 0))),
            'cost_per_inline_link_click': calculate_delta(float(last_7_days_data.get('cost_per_inline_link_click', 0)), float(last_7_days_delta_data.get('cost_per_inline_link_click', 0))),
            'ctr': calculate_delta(float(last_7_days_data.get('ctr', 0)), float(last_7_days_delta_data.get('ctr', 0))),
            'actions': last_7_days_delta_data.get('actions', 0),
        }
        if last_7_days_delta_data.get('purchase_roas', 0) == 0:
            last_7_days_delta_data['purchase_roas'] = 0
        else:
            last_7_days_delta_result['purchase_roas'] = calculate_delta(float(last_7_days_data.get('purchase_roas', 0)[0]['value']), float(last_7_days_delta_data.get('purchase_roas', 0)[0]['value'])) 
        if last_7_days_delta_data.get('outbound_clicks_ctr', 0) == 0:
            last_7_days_delta_data['outbound_clicks_ctr'] = 0
        else:
            last_7_days_delta_result['outbound_clicks_ctr'] = calculate_delta(float(last_7_days_data.get('outbound_clicks_ctr', 0)[0]['value']), float(last_7_days_delta_data.get('outbound_clicks_ctr', 0)[0]['value'])) 
        for action in last_7_days_delta_result['actions']:
            if action['action_type'] == 'purchase':
                last_7_days_delta_result['result'] = int(last_7_days_result['result']) - int(action['value'])
                break

        cache.set(last_7_days_cache_key, last_7_days_result)
        cache.set(last_7_days_delta_cache_key, last_7_days_delta_result)

    # last 30 days cacheing

    last_30_days_cache_key = f'last_30_days_result_{str(id)}'
    last_30_days_delta_cache_key = f'last_30_days_delta_result_{str(id)}'
    last_30_days_result = cache.get(last_30_days_cache_key)
    last_30_days_delta_result = cache.get(last_30_days_delta_cache_key)

    if last_30_days_result is None:
        last_30_days_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days),
                    'until': str(today),
                },
                'level': 'account',
            }
        )
        last_30_days_data = last_30_days_insights[0]
        last_30_days_result = {
            'spend': round(float(last_30_days_data.get('spend', 0)),3),
            'cpm': round(float(last_30_days_data.get('cpm', 0)),3),
            'impressions': last_30_days_data.get('impressions', 0),
            'actions': last_30_days_data.get('actions', 0),
            'reach': last_30_days_data.get('reach', 0),
            'frequency': round(float(last_30_days_data.get('frequency', 0)),3),
            'cpc': round(float(last_30_days_data.get('cpc', 0)),3),
            'cost_per_inline_link_click': round(float(last_30_days_data.get('cost_per_inline_link_click', 0)),3),
            'ctr': round(float(last_30_days_data.get('ctr', 0)),3),
        }
        if last_30_days_data.get('purchase_roas', 0) == 0:
            last_30_days_result['purchase_roas'] = 0
        else:
            last_30_days_result['purchase_roas'] = round(float(last_30_days_data.get('purchase_roas')[0]['value']),3) 
        if last_30_days_data.get('outbound_clicks_ctr', 0) == 0:
            last_30_days_result['outbound_clicks_ctr'] = 0
        else:
            last_30_days_result['outbound_clicks_ctr'] = round(float(last_30_days_data.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in last_30_days_result['actions']:
            if action['action_type'] == 'purchase':
                last_30_days_result['result'] = action['value']
                break
        last_30_days_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days_delta),
                    'until': str(last_30_days - timedelta(days=1)),
                },
                'level': 'account',
            }
        )
        last_30_days_delta_data = last_30_days_delta_insights[0]
        last_30_days_delta_result = {
            'spend': calculate_delta(float(last_30_days_data.get('spend', 0)) , float(last_30_days_delta_data.get('spend', 0))),
            'cpm': calculate_delta(float(last_30_days_data.get('cpm', 0)) , float(last_30_days_delta_data.get('cpm', 0))),
            'impressions': calculate_delta(int(last_30_days_data.get('impressions', 0)), int(last_30_days_delta_data.get('impressions', 0))),
            'reach': calculate_delta(int(last_30_days_data.get('reach', 0)), int(last_30_days_delta_data.get('reach', 0))),
            'frequency': calculate_delta(float(last_30_days_data.get('frequency', 0)), float(last_30_days_delta_data.get('frequency', 0))),
            'cpc': calculate_delta(float(last_30_days_data.get('cpc', 0)), float(last_30_days_delta_data.get('cpc', 0))),
            'cost_per_inline_link_click': calculate_delta(float(last_30_days_data.get('cost_per_inline_link_click', 0)), float(last_30_days_delta_data.get('cost_per_inline_link_click', 0))),
            'ctr': calculate_delta(float(last_30_days_data.get('ctr', 0)), float(last_30_days_delta_data.get('ctr', 0))),
            'actions': last_30_days_delta_data.get('actions', 0),
        }
        if last_30_days_delta_data.get('purchase_roas', 0) == 0:
            last_30_days_delta_data['purchase_roas'] = 0
        else:
            last_30_days_delta_result['purchase_roas'] = calculate_delta(float(last_30_days_data.get('purchase_roas', 0)[0]['value']), float(last_30_days_delta_data.get('purchase_roas', 0)[0]['value'])) 
        if last_30_days_delta_data.get('outbound_clicks_ctr', 0) == 0:
            last_30_days_delta_data['outbound_clicks_ctr'] = 0
        else:
            last_30_days_delta_result['outbound_clicks_ctr'] = calculate_delta(float(last_30_days_data.get('outbound_clicks_ctr', 0)[0]['value']), float(last_30_days_delta_data.get('outbound_clicks_ctr', 0)[0]['value'])) 
        for action in last_30_days_delta_result['actions']:
            if action['action_type'] == 'purchase':
                last_30_days_delta_result['result'] = int(last_30_days_result['result']) - int(action['value'])
                break
        
        cache.set(last_30_days_cache_key, last_30_days_result)
        cache.set(last_30_days_delta_cache_key, last_30_days_delta_result)

    return render(request, 'myapp/facebook/account.html',{
        'yesterday': yesterday_result,
        'last_3_days': last_3_days_result,
        'last_7_days': last_7_days_result,
        'last_30_days': last_30_days_result,
        'yesterday_delta': yesterday_delta_result,
        'last_3_days_delta': last_3_days_delta_result,
        'last_7_days_delta': last_7_days_delta_result,
        'last_30_days_delta': last_30_days_delta_result,
    })


