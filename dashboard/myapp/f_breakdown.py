from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import render
from datetime import datetime, timedelta, date
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from myapp.f_account import calculate_delta
from dotenv import load_dotenv
import os
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

# Age Breakdown //////////////////////////////////////////////////////////////////////////////////////////////
@cache_page(60*60)
def breakdown_age(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))




    # yesterday age breakdown delta and cacheing

    yesterday_cache_key = f'yesterday_age_breakdown_{str(id)}'
    yesterday_age_breakdown = cache.get(yesterday_cache_key)

    if yesterday_age_breakdown is None:
        yesterday_age_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        yesterday_age_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday_delta),
                    'until': str(yesterday_delta),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        yesterday_age_breakdown = []

        for insights in yesterday_age_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['age'] = insights.get('age', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_age_breakdown for _age_breakdown in yesterday_age_breakdown_delta_insights if _age_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            yesterday_age_breakdown.append(data)
            yesterday_age_breakdown.pop()

        cache.set(yesterday_cache_key, yesterday_age_breakdown)

    
    
    # last 3 days age breakdown delta and cacheing

    last_3_days_cache_key = f'last_3_days_age_breakdown_{str(id)}'
    last_3_days_age_breakdown = cache.get(last_3_days_cache_key)

    if last_3_days_age_breakdown is None:
        last_3_days_age_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        last_3_days_age_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days_delta),
                    'until': str(last_3_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        last_3_days_age_breakdown = []

        for insights in last_3_days_age_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['age'] = insights.get('age', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_age_breakdown for _age_breakdown in last_3_days_age_breakdown_delta_insights if _age_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_3_days_age_breakdown.append(data)
            last_3_days_age_breakdown.pop()
        
        cache.set(last_3_days_cache_key, last_3_days_age_breakdown)



    # last 7 days age breakdown delta and cacheing

    last_7_days_cache_key = f'last_7_days_age_breakdown_{str(id)}'
    last_7_days_age_breakdown = cache.get(last_7_days_cache_key)

    if last_7_days_age_breakdown is None:
        last_7_days_age_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        last_7_days_age_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days_delta),
                    'until': str(last_7_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        last_7_days_age_breakdown = []

        for insights in last_7_days_age_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['age'] = insights.get('age', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_age_breakdown for _age_breakdown in last_7_days_age_breakdown_delta_insights if _age_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_7_days_age_breakdown.append(data)
            last_7_days_age_breakdown.pop()

        cache.set(last_7_days_cache_key, last_7_days_age_breakdown)



    # last 30 days age breakdown delta and cacheing

    last_30_days_cache_key = f'last_30_days_age_breakdown_{str(id)}'
    last_30_days_age_breakdown = cache.get(last_30_days_cache_key)

    if last_30_days_age_breakdown is None:
        last_30_days_age_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        last_30_days_age_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days_delta),
                    'until': str(last_30_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'age',
            }
        )
        last_30_days_age_breakdown = []
        
        for insights in last_30_days_age_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['age'] = insights.get('age', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_age_breakdown for _age_breakdown in last_30_days_age_breakdown_delta_insights if _age_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_30_days_age_breakdown.append(data)
            last_30_days_age_breakdown.pop()
        
        cache.set(last_30_days_cache_key, last_30_days_age_breakdown)



    return render(request, 'myapp/facebook/breakdown_age.html',{
        'yesterday_age_breakdown' : yesterday_age_breakdown,
        'last_3_days_age_breakdown' : last_3_days_age_breakdown,
        'last_7_days_age_breakdown' : last_7_days_age_breakdown,
        'last_30_days_age_breakdown' : last_30_days_age_breakdown,
    })


# Gender Breakdown /////////////////////////////////////////////////////////////////////////////////////////////////
@cache_page(60*60)
def breakdown_gender(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))


    # yesterday gender breaksown delta and cacheing

    yesterday_cache_key = f'yesterday_gender_breakdown_{str(id)}'
    yesterday_gender_breakdown = cache.get(yesterday_cache_key)

    if yesterday_gender_breakdown is None:
        yesterday_gender_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        yesterday_gender_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday_delta),
                    'until': str(yesterday_delta),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        yesterday_gender_breakdown = []

        for insights in yesterday_gender_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['gender'] = insights.get('gender', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_gender_breakdown for _gender_breakdown in yesterday_gender_breakdown_delta_insights if _gender_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            yesterday_gender_breakdown.append(data)
        
        cache.set(yesterday_cache_key, yesterday_gender_breakdown)


    # last_3_days gender breaksown delta and cacheing

    last_3_days_cache_key = f'last_3_days_gender_breakdown_{str(id)}'
    last_3_days_gender_breakdown = cache.get(last_3_days_cache_key)

    if last_3_days_gender_breakdown is None:
        last_3_days_gender_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        last_3_days_gender_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days_delta),
                    'until': str(last_3_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        last_3_days_gender_breakdown = []

        for insights in last_3_days_gender_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['gender'] = insights.get('gender', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_gender_breakdown for _gender_breakdown in last_3_days_gender_breakdown_delta_insights if _gender_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_3_days_gender_breakdown.append(data)
        
        cache.set(last_3_days_cache_key, last_3_days_gender_breakdown)
    

    # last_7_days gender breaksown delta and cacheing

    last_7_days_cache_key = f'last_7_days_gender_breakdown_{str(id)}'
    last_7_days_gender_breakdown = cache.get(last_7_days_cache_key)

    if last_7_days_gender_breakdown is None:
        last_7_days_gender_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        last_7_days_gender_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days_delta),
                    'until': str(last_7_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        last_7_days_gender_breakdown = []

        for insights in last_7_days_gender_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['gender'] = insights.get('gender', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_gender_breakdown for _gender_breakdown in last_7_days_gender_breakdown_delta_insights if _gender_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_7_days_gender_breakdown.append(data)

        cache.set(last_7_days_cache_key, last_7_days_gender_breakdown)


    # last_30_days gender breaksown delta and cacheing

    last_30_days_cache_key = f'last_30_days_gender_breakdown_{str(id)}'
    last_30_days_gender_breakdown = cache.get(last_30_days_cache_key)

    if last_30_days_gender_breakdown is None:
        last_30_days_gender_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        last_30_days_gender_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days_delta),
                    'until': str(last_30_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'gender',
            }
        )
        last_30_days_gender_breakdown = []

        for insights in last_30_days_gender_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['gender'] = insights.get('gender', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_gender_breakdown for _gender_breakdown in last_30_days_gender_breakdown_delta_insights if _gender_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_30_days_gender_breakdown.append(data)
        
        cache.set(last_30_days_cache_key, last_30_days_gender_breakdown)

    return render(request, 'myapp/facebook/breakdown_gender.html',{
        'yesterday_gender_breakdown' : yesterday_gender_breakdown,
        'last_3_days_gender_breakdown' : last_3_days_gender_breakdown,
        'last_7_days_gender_breakdown' : last_7_days_gender_breakdown,
        'last_30_days_gender_breakdown' : last_30_days_gender_breakdown,
    })




# Platform Breakdown ///////////////////////////////////////////////////////////////////////////////////////
@cache_page(60*60)
def breakdown_platform(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))



    # yesterday platform breaksown delta and cacheing

    yesterday_cache_key = f'yesterday_platform_breakdown_{str(id)}'
    yesterday_platform_breakdown = cache.get(yesterday_cache_key)

    if yesterday_platform_breakdown is None:
        yesterday_platform_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        yesterday_platform_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday_delta),
                    'until': str(yesterday_delta),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        yesterday_platform_breakdown = []

        for insights in yesterday_platform_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_platform_breakdown for _platform_breakdown in yesterday_platform_breakdown_delta_insights if _platform_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            yesterday_platform_breakdown.append(data)
        
        cache.set(yesterday_cache_key, yesterday_platform_breakdown)


    # last_3_days platform breaksown delta and cacheing

    last_3_days_cache_key = f'last_3_days_platform_breakdown_{str(id)}'
    last_3_days_platform_breakdown = cache.get(last_3_days_cache_key)

    if last_3_days_platform_breakdown is None:
        last_3_days_platform_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        last_3_days_platform_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days_delta),
                    'until': str(last_3_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        last_3_days_platform_breakdown = []

        for insights in last_3_days_platform_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_platform_breakdown for _platform_breakdown in last_3_days_platform_breakdown_delta_insights if _platform_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_3_days_platform_breakdown.append(data)

        cache.set(last_3_days_cache_key, last_3_days_platform_breakdown)


    # last_7_days platform breaksown delta and cacheing

    last_7_days_cache_key = f'last_7_days_platform_breakdown_{str(id)}'
    last_7_days_platform_breakdown = cache.get(last_7_days_cache_key)

    if last_7_days_platform_breakdown is None:
        last_7_days_platform_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        last_7_days_platform_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days_delta),
                    'until': str(last_7_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        last_7_days_platform_breakdown = []

        for insights in last_7_days_platform_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_platform_breakdown for _platform_breakdown in last_7_days_platform_breakdown_delta_insights if _platform_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_7_days_platform_breakdown.append(data)

        cache.set(last_7_days_cache_key, last_7_days_platform_breakdown)



    # last_30_days platform breaksown delta and cacheing

    last_30_days_cache_key = f'last_30_days_platform_breakdown_{str(id)}'
    last_30_days_platform_breakdown = cache.get(last_30_days_cache_key)

    if last_30_days_platform_breakdown is None:
        last_30_days_platform_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        last_30_days_platform_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days_delta),
                    'until': str(last_30_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform',
            }
        )
        last_30_days_platform_breakdown = []
        
        for insights in last_30_days_platform_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_platform_breakdown for _platform_breakdown in last_30_days_platform_breakdown_delta_insights if _platform_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_30_days_platform_breakdown.append(data)

        cache.set(last_30_days_cache_key, last_30_days_platform_breakdown)
    
    return render(request, 'myapp/facebook/breakdown_platform.html',{
       'yesterday_platform_breakdown' : yesterday_platform_breakdown,
       'last_3_days_platform_breakdown' : last_3_days_platform_breakdown,
       'last_7_days_platform_breakdown' : last_7_days_platform_breakdown,
       'last_30_days_platform_breakdown' : last_30_days_platform_breakdown,
    })



# Placement Breakdown ///////////////////////////////////////////////////////////////////////////////////////
@cache_page(60*60)
def breakdown_placement(request, id):
    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    account = AdAccount(str(id))



    # yesterday placement breaksown delta and cacheing

    yesterday_cache_key = f'yesterday_placement_breakdown_{str(id)}'
    yesterday_placement_breakdown = cache.get(yesterday_cache_key)

    if yesterday_placement_breakdown is None:
        yesterday_placement_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        yesterday_placement_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(yesterday_delta),
                    'until': str(yesterday_delta),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        yesterday_placement_breakdown = []

        for insights in yesterday_placement_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            data['platform_position'] = insights.get('platform_position', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_placement_breakdown for _placement_breakdown in yesterday_placement_breakdown_delta_insights if _placement_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            yesterday_placement_breakdown.append(data)

        cache.set(yesterday_cache_key, yesterday_placement_breakdown)


    # last_3_days placement breaksown delta and cacheing

    last_3_days_cache_key = f'last_3_days_placement_breakdown_{str(id)}'
    last_3_days_placement_breakdown = cache.get(last_3_days_cache_key)

    if last_3_days_placement_breakdown is None:
        last_3_days_placement_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        last_3_days_placement_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_3_days_delta),
                    'until': str(last_3_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        last_3_days_placement_breakdown = []

        for insights in last_3_days_placement_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            data['platform_position'] = insights.get('platform_position', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_placement_breakdown for _placement_breakdown in last_3_days_placement_breakdown_delta_insights if _placement_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_3_days_placement_breakdown.append(data)

        cache.set(last_3_days_cache_key, last_3_days_placement_breakdown)

    
    # last_7_days placement breaksown delta and cacheing

    last_7_days_cache_key = f'last_7_days_placement_breakdown_{str(id)}'
    last_7_days_placement_breakdown = cache.get(last_7_days_cache_key)

    if last_7_days_placement_breakdown is None:
        last_7_days_placement_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        last_7_days_placement_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_7_days_delta),
                    'until': str(last_7_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        last_7_days_placement_breakdown = []

        for insights in last_7_days_placement_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            data['platform_position'] = insights.get('platform_position', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_placement_breakdown for _placement_breakdown in last_7_days_placement_breakdown_delta_insights if _placement_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_7_days_placement_breakdown.append(data)
        
        cache.set(last_7_days_cache_key, last_7_days_placement_breakdown)



    # last_30_days placement breaksown delta and cacheing

    last_30_days_cache_key = f'last_30_days_placement_breakdown_{str(id)}'
    last_30_days_placement_breakdown = cache.get(last_30_days_cache_key)

    if last_30_days_placement_breakdown is None:
        last_30_days_placement_breakdown_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days),
                    'until': str(today),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        last_30_days_placement_breakdown_delta_insights = account.get_insights(
            fields=fields,
            params={
                'time_range': {
                    'since': str(last_30_days_delta),
                    'until': str(last_30_days - timedelta(days=1)),
                },
                'level': 'account',
                'breakdowns': 'publisher_platform, platform_position',
            }
        )
        last_30_days_placement_breakdown = []

        for insights in last_30_days_placement_breakdown_insights:
            data = {}
            data['id'] = insights.get('account_id', '')
            data['name'] = insights.get('accoint_name', '')
            data['impressions'] = insights.get('impressions', 0)
            data['reach'] = insights.get('reach', 0)
            data['spend'] = insights.get('spend', 0)
            data['frequency'] = round(float(insights.get('frequency', 0)),2)
            data['actions'] = insights.get('actions', [])
            data['cost_per_inline_link_click'] = round(float(insights.get('cost_per_inline_link_click', 0)),2)
            data['cpm'] = round(float(insights.get('cpm', 0)),2)
            data['cpc'] = round(float(insights.get('cpc', 0)),2)
            data['ctr'] = round(float(insights.get('ctr', 0)),2)
            data['impressions'] = insights.get('impressions', 0)
            data['publisher_platform'] = insights.get('publisher_platform', '')
            data['platform_position'] = insights.get('platform_position', '')
            if 'purchase_roas' in insights and isinstance(insights['purchase_roas'], list) and len(insights['purchase_roas']) > 0:
                data['purchase_roas'] = round(float(insights['purchase_roas'][0]['value']), 2)
            else:
                data['purchase_roas'] = 0
            if 'outbound_clicks_ctr' in insights and isinstance(insights['outbound_clicks_ctr'], list) and len(insights['outbound_clicks_ctr']) > 0:
                data['outbound_clicks_ctr'] = round(float(insights['outbound_clicks_ctr'][0]['value']), 2)
            else:
                data['outbound_clicks_ctr'] = 0
            data['result'] = 0 
            for action in data['actions']:
                if action['action_type'] == 'purchase':
                    data['result'] = action['value']

            corresponding_insight = next(
                (_placement_breakdown for _placement_breakdown in last_30_days_placement_breakdown_delta_insights if _placement_breakdown.get('account_id') == data['id']),
                None
            )

            if corresponding_insight:
                _impressions = corresponding_insight.get('impressions', 0)
                _reach = corresponding_insight.get('reach', 0)
                _spend = corresponding_insight.get('spend', 0)
                _frequency = corresponding_insight.get('frequency', 0)
                _cost_per_inline_link_click = corresponding_insight.get('cost_per_inline_link_click', 0)
                _cpm = corresponding_insight.get('cpm', 0)
                _cpc = corresponding_insight.get('cpc', 0)
                _ctr = corresponding_insight.get('ctr', 0)
                _purchase_roas = corresponding_insight.get('purchase_roas', 0)
                _outbound_clicks_ctr = corresponding_insight.get('outbound_clicks_ctr', 0)
                _actions = corresponding_insight.get('actions', [])
                data['delta_impressions'] = calculate_delta(int(data['impressions']), int(_impressions))
                data['delta_spend'] = round(calculate_delta(float(data['spend']), float(_spend)), 2)
                data['delta_reach'] = calculate_delta(int(data['reach']), int(_reach))
                data['delta_frequency'] = round(calculate_delta(float(data['frequency']), float(_frequency)), 2)
                data['delta_cost_per_inline_link_click'] = round(calculate_delta(float(data['cost_per_inline_link_click']), float(_cost_per_inline_link_click)), 2)
                data['delta_cpm'] = round(calculate_delta(float(data['cpm']), float(_cpm)), 2)
                data['delta_cpc'] = round(calculate_delta(float(data['cpc']), float(_cpc)), 2)
                data['delta_ctr'] = round(calculate_delta(float(data['ctr']), float(_ctr)), 2)
                if 'purchase_roas' in corresponding_insight and isinstance(_purchase_roas, list) and len(_purchase_roas) > 0:
                    data['delta_purchase_roas'] = round(calculate_delta(float(data['purchase_roas']), float(_purchase_roas[0]['value'])), 2)
                else:
                    data['delta_purchase_roas'] = 0
                if 'outbound_clicks_ctr' in corresponding_insight and isinstance(_outbound_clicks_ctr, list) and len(_outbound_clicks_ctr) > 0:
                    data['delta_outbound_clicks_ctr'] = round(calculate_delta(float(data['outbound_clicks_ctr']), float(_outbound_clicks_ctr[0]['value'])), 2)
                else:
                    data['delta_outbound_clicks_ctr'] = 0
                for action in _actions:
                    if action['action_type'] == 'purchase':
                        data['delta_result'] = round(calculate_delta(float(data['result']), float(action['value'])), 2)
            last_30_days_placement_breakdown.append(data)
        
        cache.set(last_30_days_cache_key, last_30_days_placement_breakdown)

    
    return render(request, 'myapp/facebook/breakdown_placement.html',{
        'yesterday_placement_breakdown' : yesterday_placement_breakdown,
        'last_3_days_placement_breakdown' : last_3_days_placement_breakdown,
        'last_7_days_placement_breakdown' : last_7_days_placement_breakdown,
        'last_30_days_placement_breakdown' : last_30_days_placement_breakdown,
    })
