from django.views.decorators.cache import cache_page
from django.core.cache import cache
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.conf import settings
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from myapp.f_account import calculate_delta
from dotenv import load_dotenv
import os
import re

load_dotenv()

today = date.today() - timedelta(days=1)
yesterday = date.today() - timedelta(days=1)
last_3_days = date.today() - timedelta(days=3)
last_7_days = date.today() - timedelta(days=7)
last_30_days = date.today() - timedelta(days=30)
yesterday_delta = date.today() - timedelta(days=2)
last_3_days_delta = date.today() - timedelta(days=6)
last_7_days_delta = date.today() - timedelta(days=14)
last_30_days_delta = date.today() - timedelta(days=60)

fields = [
    'campaign_id',
    'campaign_name',
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

@cache_page(60 * 600)
def campaign_insights(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))

    account_id = re.sub(r'\D', '', id)
    business_id = os.environ['BUSINESS_ID']
    app_id = os.environ['APP_ID']
    

    # yesterday campaign cacheing

    yesterday_cache_key = f'yesterday_campaigns_{str(id)}'
    yesterday_campaigns = cache.get(yesterday_cache_key)

    if yesterday_campaigns is None:
        yesterday_campaign_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday),
                    'until': str(today),
                },
                'level': 'campaign',
            }
        )
        yesterday_campaign_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday_delta),
                    'until': str(yesterday_delta),
                },
                'level': 'campaign',
            }
        )
        yesterday_campaigns = []
        for insight in yesterday_campaign_insights:
            data = {}
            data['id'] = insight.get('campaign_id', '')
            data['name'] = insight.get('campaign_name', '')
            data['objective'] = insight.get('objective', '')
            data['impressions'] = insight.get('impressions', 0)
            data['reach'] = insight.get('reach', 0)
            data['spend'] = insight.get('spend', 0)
            data['frequency'] = round(float(insight.get('frequency', 0)),2)
            data['actions'] = insight.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insight.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insight.get('cpm', 0)),2)
            data['cpc'] = round(float(insight.get('cpc', 0)),2)
            data['ctr'] = round(float(insight.get('ctr', 0)),2)
            if 'purchase_roas' in insight and isinstance(insight['purchase_roas'], list) and len(insight['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insight['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insight and isinstance(insight['outbound_clicks_ctr'], list) and len(insight['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insight['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0  # Initialize 'result' key to 0
            data['views'] = 0  # Initialize 'views' key to 0
            data['addtocart'] = 0  # Initialize 'addtocart' key to 0
            data['checkout'] = 0  # Initialize 'checkout' key to 0
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']
                if action['action_type'] == 'view_content':
                    data['views'] = action['value']
                if action['action_type'] == 'add_to_cart':
                    data['addtocart'] = action['value']
                if action['action_type'] == 'initiate_checkout':
                    data['checkout'] = action['value']
            corresponding_campaign = next(
                (_campaign for _campaign in yesterday_campaign_delta_insights if _campaign.get('campaign_id') == data['id']),
                None
            )
            if corresponding_campaign:
                _impressions = corresponding_campaign.get('impressions', 0)
                _reach = corresponding_campaign.get('reach', 0)
                _spend = corresponding_campaign.get('spend', 0)
                _frequency = corresponding_campaign.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_campaign.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_campaign.get('cpm', 0)
                _cpc = corresponding_campaign.get('cpc', 0)
                _ctr = corresponding_campaign.get('ctr', 0)
                _purchase_roas = corresponding_campaign.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_campaign.get('outbound_clicks_ctr', 0)
                _actions = corresponding_campaign.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_campaign and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_campaign and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
                    if action['action_type'] == 'view_content':
                        data['delta_views'] = round(calculate_delta(float(data['views']), float(action['value'])), 2)
                    if action['action_type'] == 'add_to_cart':
                        data['delta_addtocart'] = round(calculate_delta(float(data['addtocart']), float(action['value'])), 2)
                    if action['action_type'] == 'initiate_checkout':
                        data['delta_checkout'] = round(calculate_delta(float(data['checkout']), float(action['value'])), 2)
            yesterday_campaigns.append(data)

        cache.set(yesterday_cache_key,yesterday_campaigns)



    #  last 3 days campaign cacheing ////////////////////////////////////////////////////////////////////

    last_3_days_cache_key = f'last_3_days_campaigns_{str(id)}'
    last_3_days_campaigns = cache.get(last_3_days_cache_key)

    if last_3_days_campaigns is None:
        last_3_days_campaign_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days),
                    'until': str(today),
                },
                'level': 'campaign',
            }
        )
        last_3_days_campaign_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days_delta),
                    'until': str(last_3_days - timedelta(days=1)),
                },
                'level': 'campaign',
            }
        )
        last_3_days_campaigns = []
        for insight in last_3_days_campaign_insights:
            data = {}
            data['id'] = insight.get('campaign_id', '')
            data['name'] = insight.get('campaign_name', '')
            data['objective'] = insight.get('objective', '')
            data['impressions'] = insight.get('impressions', 0)
            data['reach'] = insight.get('reach', 0)
            data['spend'] = insight.get('spend', 0)
            data['frequency'] = round(float(insight.get('frequency', 0)),2)
            data['actions'] = insight.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insight.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insight.get('cpm', 0)),2)
            data['cpc'] = round(float(insight.get('cpc', 0)),2)
            data['ctr'] = round(float(insight.get('ctr', 0)),2)
            if 'purchase_roas' in insight and isinstance(insight['purchase_roas'], list) and len(insight['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insight['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insight and isinstance(insight['outbound_clicks_ctr'], list) and len(insight['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insight['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0  # Initialize 'result' key to 0
            data['views'] = 0  # Initialize 'views' key to 0
            data['addtocart'] = 0  # Initialize 'addtocart' key to 0
            data['checkout'] = 0  # Initialize 'checkout' key to 0
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']
                if action['action_type'] == 'view_content':
                    data['views'] = action['value']
                if action['action_type'] == 'add_to_cart':
                    data['addtocart'] = action['value']
                if action['action_type'] == 'initiate_checkout':
                    data['checkout'] = action['value']
            corresponding_campaign = next(
                (_campaign for _campaign in last_3_days_campaign_delta_insights if _campaign.get('campaign_id') == data['id']),
                None
            )
            if corresponding_campaign:
                _impressions = corresponding_campaign.get('impressions', 0)
                _reach = corresponding_campaign.get('reach', 0)
                _spend = corresponding_campaign.get('spend', 0)
                _frequency = corresponding_campaign.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_campaign.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_campaign.get('cpm', 0)
                _cpc = corresponding_campaign.get('cpc', 0)
                _ctr = corresponding_campaign.get('ctr', 0)
                _purchase_roas = corresponding_campaign.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_campaign.get('outbound_clicks_ctr', 0)
                _actions = corresponding_campaign.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_campaign and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_campaign and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
                    if action['action_type'] == 'view_content':
                        data['delta_views'] = round(calculate_delta(float(data['views']), float(action['value'])), 2)
                    if action['action_type'] == 'add_to_cart':
                        data['delta_addtocart'] = round(calculate_delta(float(data['addtocart']), float(action['value'])), 2)
                    if action['action_type'] == 'initiate_checkout':
                        data['delta_checkout'] = round(calculate_delta(float(data['checkout']), float(action['value'])), 2)
            last_3_days_campaigns.append(data)
        
        cache.set(last_3_days_cache_key,last_3_days_campaigns)




    #  last 7 days campaign cacheing ////////////////////////////////////////////////////////////////////

    last_7_days_cache_key = f'last_7_days_campaigns_{str(id)}'
    last_7_days_campaigns = cache.get(last_7_days_cache_key)

    if last_7_days_campaigns is None:
        last_7_days_campaign_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days),
                    'until': str(today),
                },
                'level': 'campaign',
            }
        )
        last_7_days_campaign_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days_delta),
                    'until': str(last_7_days - timedelta(days=1)),
                },
                'level': 'campaign',
            }
        )
        last_7_days_campaigns = []
        for insight in last_7_days_campaign_insights:
            data = {}
            data['id'] = insight.get('campaign_id', '')
            data['name'] = insight.get('campaign_name', '')
            data['objective'] = insight.get('objective', '')
            data['impressions'] = insight.get('impressions', 0)
            data['reach'] = insight.get('reach', 0)
            data['spend'] = insight.get('spend', 0)
            data['frequency'] = round(float(insight.get('frequency', 0)),2)
            data['actions'] = insight.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insight.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insight.get('cpm', 0)),2)
            data['cpc'] = round(float(insight.get('cpc', 0)),2)
            data['ctr'] = round(float(insight.get('ctr', 0)),2)
            if 'purchase_roas' in insight and isinstance(insight['purchase_roas'], list) and len(insight['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insight['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insight and isinstance(insight['outbound_clicks_ctr'], list) and len(insight['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insight['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0  # Initialize 'result' key to 0
            data['views'] = 0  # Initialize 'views' key to 0
            data['addtocart'] = 0  # Initialize 'addtocart' key to 0
            data['checkout'] = 0  # Initialize 'checkout' key to 0
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']
                if action['action_type'] == 'view_content':
                    data['views'] = action['value']
                if action['action_type'] == 'add_to_cart':
                    data['addtocart'] = action['value']
                if action['action_type'] == 'initiate_checkout':
                    data['checkout'] = action['value']
            corresponding_campaign = next(
                (_campaign for _campaign in last_7_days_campaign_delta_insights if _campaign.get('campaign_id') == data['id']),
                None
            )
            if corresponding_campaign:
                _impressions = corresponding_campaign.get('impressions', 0)
                _reach = corresponding_campaign.get('reach', 0)
                _spend = corresponding_campaign.get('spend', 0)
                _frequency = corresponding_campaign.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_campaign.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_campaign.get('cpm', 0)
                _cpc = corresponding_campaign.get('cpc', 0)
                _ctr = corresponding_campaign.get('ctr', 0)
                _purchase_roas = corresponding_campaign.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_campaign.get('outbound_clicks_ctr', 0)
                _actions = corresponding_campaign.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_campaign and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_campaign and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
                    if action['action_type'] == 'view_content':
                        data['delta_views'] = round(calculate_delta(float(data['views']), float(action['value'])), 2)
                    if action['action_type'] == 'add_to_cart':
                        data['delta_addtocart'] = round(calculate_delta(float(data['addtocart']), float(action['value'])), 2)
                    if action['action_type'] == 'initiate_checkout':
                        data['delta_checkout'] = round(calculate_delta(float(data['checkout']), float(action['value'])), 2)
            last_7_days_campaigns.append(data)
        
        cache.set(last_7_days_cache_key,last_7_days_campaigns)




    #  last 30 days campaign cacheing ////////////////////////////////////////////////////////////////////

    last_30_days_cache_key = f'last_30_days_campaigns_{str(id)}'
    last_30_days_campaigns = cache.get(last_30_days_cache_key)

    if last_30_days_campaigns is None:
        last_30_days_campaign_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days),
                    'until': str(today),
                },
                'level': 'campaign',
            }
        )
        last_30_days_campaign_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days_delta),
                    'until': str(last_30_days - timedelta(days=1)),
                },
                'level': 'campaign',
            }
        )
        last_30_days_campaigns = []
        for insight in last_30_days_campaign_insights:
            data = {}
            data['id'] = insight.get('campaign_id', '')
            data['name'] = insight.get('campaign_name', '')
            data['objective'] = insight.get('objective', '')
            data['impressions'] = insight.get('impressions', 0)
            data['reach'] = insight.get('reach', 0)
            data['spend'] = insight.get('spend', 0)
            data['frequency'] = round(float(insight.get('frequency', 0)),2)
            data['actions'] = insight.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insight.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insight.get('cpm', 0)),2)
            data['cpc'] = round(float(insight.get('cpc', 0)),2)
            data['ctr'] = round(float(insight.get('ctr', 0)),2)
            if 'purchase_roas' in insight and isinstance(insight['purchase_roas'], list) and len(insight['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insight['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insight and isinstance(insight['outbound_clicks_ctr'], list) and len(insight['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insight['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0  # Initialize 'result' key to 0
            data['views'] = 0  # Initialize 'views' key to 0
            data['addtocart'] = 0  # Initialize 'addtocart' key to 0
            data['checkout'] = 0  # Initialize 'checkout' key to 0
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']
                if action['action_type'] == 'view_content':
                    data['views'] = action['value']
                if action['action_type'] == 'add_to_cart':
                    data['addtocart'] = action['value']
                if action['action_type'] == 'initiate_checkout':
                    data['checkout'] = action['value']
            corresponding_campaign = next(
                (_campaign for _campaign in last_30_days_campaign_delta_insights if _campaign.get('campaign_id') == data['id']),
                None
            )
            if corresponding_campaign:
                _impressions = corresponding_campaign.get('impressions', 0)
                _reach = corresponding_campaign.get('reach', 0)
                _spend = corresponding_campaign.get('spend', 0)
                _frequency = corresponding_campaign.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_campaign.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_campaign.get('cpm', 0)
                _cpc = corresponding_campaign.get('cpc', 0)
                _ctr = corresponding_campaign.get('ctr', 0)
                _purchase_roas = corresponding_campaign.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_campaign.get('outbound_clicks_ctr', 0)
                _actions = corresponding_campaign.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_campaign and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_campaign and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
                    if action['action_type'] == 'view_content':
                        data['delta_views'] = round(calculate_delta(float(data['views']), float(action['value'])), 2)
                    if action['action_type'] == 'add_to_cart':
                        data['delta_addtocart'] = round(calculate_delta(float(data['addtocart']), float(action['value'])), 2)
                    if action['action_type'] == 'initiate_checkout':
                        data['delta_checkout'] = round(calculate_delta(float(data['checkout']), float(action['value'])), 2)
            last_30_days_campaigns.append(data)
        
        cache.set(last_30_days_cache_key,last_30_days_campaigns)



    # for campaign in yesterday_campaign_insights:
    # print(yesterday_campaigns)


    return render(request, 'myapp/facebook/campaigns.html', {
        'yesterday_campaigns': yesterday_campaigns,
        'last_3_days_campaigns': last_3_days_campaigns,
        'last_7_days_campaigns': last_7_days_campaigns,
        'last_30_days_campaigns': last_30_days_campaigns,
        'account_id': account_id,
        'business_id': business_id,
        'app_id' : app_id,
    })