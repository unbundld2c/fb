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
    'campaign_name',
    'campaign_id',
    'adset_id',
    'adset_name',
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

@cache_page(60*60)
def adset_insights(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))

    account_id = re.sub(r'\D', '', id)
    business_id = os.environ['BUSINESS_ID']
    app_id = os.environ['APP_ID']


    # yesterday adset with delta and cacheing

    yesterday_cache_key = f'yesterday_adsets_{str(id)}'
    yesterday_adsets = cache.get(yesterday_cache_key)

    if yesterday_adsets is None:
        yesterday_adset_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday),
                    'until': str(today),
                },
                'level': 'adset',
            }
        )
        yesterday_adset_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday_delta),
                    'until': str(yesterday_delta),
                },
                'level': 'adset',
            }
        )
        yesterday_adsets = []
        for insight in yesterday_adset_insights:
            data = {}
            data['id'] = insight.get('adset_id', '')
            data['name'] = insight.get('adset_name', '')
            data['cname'] = insight.get('campaign_name', '')
            data['cid'] = insight.get('campaign_id', '')
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

            corresponding_adset = next(
                (_adset for _adset in yesterday_adset_delta_insights if _adset.get('adset_id') == insight.get('adset_id', '')),
                None
            )

            if corresponding_adset:
                _impressions = corresponding_adset.get('impressions', 0)
                _reach = corresponding_adset.get('reach', 0)
                _spend = corresponding_adset.get('spend', 0)
                _frequency = corresponding_adset.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_adset.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_adset.get('cpm', 0)
                _cpc = corresponding_adset.get('cpc', 0)
                _ctr = corresponding_adset.get('ctr', 0)
                _purchase_roas = corresponding_adset.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_adset.get('outbound_clicks_ctr', 0)
                _actions = corresponding_adset.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_adset and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_adset and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
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

            yesterday_adsets.append(data)

        cache.set(yesterday_cache_key, yesterday_adsets)

    # last 3 days adset insights with delta and cacheing

    last_3_days_cache_key = f'last_3_days_adsets_{str(id)}'
    last_3_days_adsets = cache.get(last_3_days_cache_key)

    if last_3_days_adsets is None:
        last_3_days_adset_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days),
                    'until': str(today),
                },
                'level': 'adset',
            }
        )
        last_3_days_adset_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days_delta),
                    'until': str(last_3_days - timedelta(days=1)),
                },
                'level': 'adset',
            }
        )
        last_3_days_adsets = []
        for insight in last_3_days_adset_insights:
            data = {}
            data['id'] = insight.get('adset_id', '')
            data['name'] = insight.get('adset_name', '')
            data['cname'] = insight.get('campaign_name', '')
            data['cid'] = insight.get('campaign_id', '')
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

            corresponding_adset = next(
                (_adset for _adset in last_3_days_adset_delta_insights if _adset.get('adset_id') == insight.get('adset_id', '')),
                None
            )

            if corresponding_adset:
                _impressions = corresponding_adset.get('impressions', 0)
                _reach = corresponding_adset.get('reach', 0)
                _spend = corresponding_adset.get('spend', 0)
                _frequency = corresponding_adset.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_adset.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_adset.get('cpm', 0)
                _cpc = corresponding_adset.get('cpc', 0)
                _ctr = corresponding_adset.get('ctr', 0)
                _purchase_roas = corresponding_adset.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_adset.get('outbound_clicks_ctr', 0)
                _actions = corresponding_adset.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_adset and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_adset and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
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
            last_3_days_adsets.append(data)
        
        cache.set(last_3_days_cache_key, last_3_days_adsets)



    # last 7 days adset insights with delta and cacheing

    last_7_days_cache_key = f'last_7_days_adsets_{str(id)}'
    last_7_days_adsets = cache.get(last_7_days_cache_key)

    if last_7_days_adsets is None:
        last_7_days_adset_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days),
                    'until': str(today),
                },
                'level': 'adset',
            }
        )
        last_7_days_adset_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days_delta),
                    'until': str(last_7_days - timedelta(days=1)),
                },
                'level': 'adset',
            }
        )
        last_7_days_adsets = []
        for insight in last_7_days_adset_insights:
            data = {}
            data['id'] = insight.get('adset_id', '')
            data['name'] = insight.get('adset_name', '')
            data['cname'] = insight.get('campaign_name', '')
            data['cid'] = insight.get('campaign_id', '')
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

            corresponding_adset = next(
                (_adset for _adset in last_7_days_adset_delta_insights if _adset.get('adset_id') == insight.get('adset_id', '')),
                None
            )

            if corresponding_adset:
                _impressions = corresponding_adset.get('impressions', 0)
                _reach = corresponding_adset.get('reach', 0)
                _spend = corresponding_adset.get('spend', 0)
                _frequency = corresponding_adset.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_adset.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_adset.get('cpm', 0)
                _cpc = corresponding_adset.get('cpc', 0)
                _ctr = corresponding_adset.get('ctr', 0)
                _purchase_roas = corresponding_adset.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_adset.get('outbound_clicks_ctr', 0)
                _actions = corresponding_adset.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_adset and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_adset and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
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

            last_7_days_adsets.append(data)

        cache.set(last_7_days_cache_key, last_7_days_adsets)



    # last 30 days adset insights with delta and cacheing

    last_30_days_cache_key = f'last_30_days_adsets_{str(id)}'
    last_30_days_adsets = cache.get(last_30_days_cache_key)

    if last_30_days_adsets is None:
        last_30_days_adset_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days),
                    'until': str(today),
                },
                'level': 'adset',
            }
        )
        last_30_days_adset_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days_delta),
                    'until': str(last_30_days - timedelta(days=1)),
                },
                'level': 'adset',
            }
        )
        last_30_days_adsets = []
        for insight in last_30_days_adset_insights:
            data = {}
            data['id'] = insight.get('adset_id', '')
            data['name'] = insight.get('adset_name', '')
            data['cname'] = insight.get('campaign_name', '')
            data['cid'] = insight.get('campaign_id', '')
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

            corresponding_adset = next(
                (_adset for _adset in last_30_days_adset_delta_insights if _adset.get('adset_id') == insight.get('adset_id', '')),
                None
            )

            if corresponding_adset:
                _impressions = corresponding_adset.get('impressions', 0)
                _reach = corresponding_adset.get('reach', 0)
                _spend = corresponding_adset.get('spend', 0)
                _frequency = corresponding_adset.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_adset.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_adset.get('cpm', 0)
                _cpc = corresponding_adset.get('cpc', 0)
                _ctr = corresponding_adset.get('ctr', 0)
                _purchase_roas = corresponding_adset.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_adset.get('outbound_clicks_ctr', 0)
                _actions = corresponding_adset.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_adset and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_adset and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
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

            last_30_days_adsets.append(data)
        
        cache.set(last_30_days_cache_key, last_30_days_adsets)
    
    

    # print(yesterday_adsets)
    return render(request, 'myapp/facebook/adsets.html', {
        'yesterday_adsets': yesterday_adsets,
        'last_3_days_adsets': last_3_days_adsets,
        'last_7_days_adsets': last_7_days_adsets,
        'last_30_days_adsets': last_30_days_adsets,
        'account_id': account_id,
        'business_id': business_id,
        'app_id' : app_id,
    })