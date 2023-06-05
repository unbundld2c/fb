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
yesterday_delta = date.today() - timedelta(days=2)
last_3_days_delta = date.today() - timedelta(days=6)
last_7_days_delta = date.today() - timedelta(days=14)
last_30_days_delta = date.today() - timedelta(days=60)

FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])

# account regular metrix/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

account_fields = [
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

def get_yesterday_regular_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(yesterday),
                'until': str(today),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

def get_last_3_days_regular_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(last_3_days),
                'until': str(today),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

def get_last_7_days_regular_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(last_7_days),
                'until': str(today),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

def get_last_30_days_regular_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(last_30_days),
                'until': str(today),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

# account delta metrix //////////////////////////////////////////////////////////////////////////////////////////////

def get_yesterday_delta_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(yesterday_delta),
                'until': str(yesterday_delta),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

def get_last_3_days_delta_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(last_3_days_delta),
                'until': str(last_3_days - timedelta(days=1)),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

def get_last_7_days_delta_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(last_7_days_delta),
                'until': str(last_7_days - timedelta(days=1)),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

def get_last_30_days_delta_metrix(id):
    account = AdAccount(str(id))
    response = account.get_insights(
        fields=account_fields,
        params={
            'time_range': {
                'since': str(last_30_days_delta),
                'until': str(last_30_days - timedelta(days=1)),
            },
            'level': 'account',
        }
    )
    data = response[0]
    result = {
        'account_name': data.get('account_name',''),
        'account_id': data.get('account_id',''),
        'spend': round(float(data.get('spend', 0)),3),
        'cpm': round(float(data.get('cpm', 0)),3),
        'impressions': data.get('impressions', 0),
        'actions': data.get('actions', 0),
        'reach': data.get('reach', 0),
        'frequency': round(float(data.get('frequency', 0)),3),
        'cpc': round(float(data.get('cpc', 0)),3),
        'cost_per_inline_link_click': round(float(data.get('cost_per_inline_link_click', 0)),3),
        'ctr': round(float(data.get('ctr', 0)),3),
    }
    if data.get('purchase_roas', 0) == 0:
        result['purchase_roas'] = 0
    else:
        result['purchase_roas'] = round(float(data.get('purchase_roas')[0]['value']),3) 
    if data.get('outbound_clicks_ctr', 0) == 0:
        result['outbound_clicks_ctr'] = 0
    else:
        result['outbound_clicks_ctr'] = round(float(data.get('outbound_clicks_ctr')[0]['value']),3) 
    for action in result['actions']:
        if action['action_type'] == 'purchase':
            result['result'] = action['value']
            break
    return result

# regular campaigns metrix ///////////////////////////////////////////////////////////////////////

campaign_fields = [
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


def get_yesterday_regular_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(yesterday),
                'until': str(today),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

def get_last_3_days_regular_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(last_3_days),
                'until': str(today),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

def get_last_7_days_regular_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(last_7_days),
                'until': str(today),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

def get_last_30_days_regular_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(last_30_days),
                'until': str(today),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

# delta campaigns metrix ////////////////////////////////////////////////////////////////////////////////////////

def get_yesterday_delta_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(yesterday_delta),
                'until': str(yesterday_delta),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

def get_last_3_days_delta_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(last_3_days_delta),
                'until': str(last_3_days - timedelta(days=1)),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

def get_last_7_days_delta_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(last_7_days_delta),
                'until': str(last_7_days - timedelta(days=1)),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

def get_last_30_days_delta_metrix_campaigns(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=campaign_fields,
        params={
            'time_range': {
                'since': str(last_30_days_delta),
                'until': str(last_30_days - timedelta(days=1)),
            },
            'level': 'campaign',
        }
    )
    capmaigns = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('campaign_id', '')
        data['name'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        capmaigns.append(data)
    return capmaigns

# adset regular metrix //////////////////////////////////////////////////////////////////

adset_fields = [
    'campaign_name',
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

def get_yesterday_regular_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(yesterday),
                'until': str(today),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

def get_last_3_days_regular_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(last_3_days),
                'until': str(today),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

def get_last_7_days_regular_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(last_7_days),
                'until': str(today),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

def get_last_30_days_regular_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(last_30_days),
                'until': str(today),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

# adsets detla metrix ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def get_yesterday_delta_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(yesterday_delta),
                'until': str(yesterday_delta),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

def get_last_3_days_delta_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(last_3_days_delta),
                'until': str(last_3_days - timedelta(days=1)),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

def get_last_7_days_delta_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(last_7_days_delta),
                'until': str(last_7_days - timedelta(days=1)),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

def get_last_30_days_delta_metrix_adsets(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=adset_fields,
        params={
            'time_range': {
                'since': str(last_30_days_delta),
                'until': str(last_30_days - timedelta(days=1)),
            },
            'level': 'adset',
        }
    )
    adsets = []
    for insight in insights:
        data = {}
        data['id'] = insight.get('adset_id', '')
        data['name'] = insight.get('adset_name', '')
        data['cname'] = insight.get('campaign_name', '')
        data['objective'] = insight.get('objective', '')
        data['impressions'] = insight.get('impressions', 0)
        data['reach'] = insight.get('reach', 0)
        data['spend'] = insight.get('spend', 0)
        data['frequency'] = insight.get('frequency', 0)
        data['actions'] = insight.get('actions', [])
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        adsets.append(data)
    return adsets

# regular ads data ////////////////////////////////////////////////////////////////////////////////////////////////////////

ads_fields = [
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

def get_yesterday_regular_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(yesterday),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads

def get_last_3_days_regular_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(last_3_days),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads

def get_last_7_days_regular_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(last_7_days),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads

def get_last_30_days_regular_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(last_30_days),
                'until': str(today),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads

# ads delta metrix /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def get_yesterday_delta_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(yesterday_delta),
                'until': str(yesterday_delta),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads

def get_last_3_days_delta_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(last_3_days_delta),
                'until': str(last_3_days - timedelta(days=1)),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads

def get_last_7_days_delta_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(last_7_days_delta),
                'until': str(last_7_days - timedelta(days=1)),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads

def get_last_30_days_delta_metrix_ads(id):
    account = AdAccount(str(id))
    insights = account.get_insights(
        fields=ads_fields,
        params={
            'time_range': {
                'since': str(last_30_days_delta),
                'until': str(last_30_days - timedelta(days=1)),
            },
            'level': 'ad',
        }
    )
    ads = []
    for insight in insights:
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
        data['cost_per_inline_link_click'] = insight.get('cost_per_inline_link_click', 0)
        data['cpm'] = insight.get('cpm', 0)
        data['cpc'] = insight.get('cpc', 0)
        data['ctr'] = insight.get('ctr', 0)
        if insight.get('purchase_roas', 0) == 0:
            data['purchase_roas'] = 0
        else:
            data['purchase_roas'] = round(float(insight.get('purchase_roas')[0]['value']),3) 
        if insight.get('outbound_clicks_ctr', 0) == 0:
            data['outbound_clicks_ctr'] = 0
        else:
            data['outbound_clicks_ctr'] = round(float(insight.get('outbound_clicks_ctr')[0]['value']),3) 
        for action in data['actions']:
            if action['action_type'] == 'purchase':
                data['result'] = action['value']
            if action['action_type'] == 'view_content':
                data['views'] = action['value']
            if action['action_type'] == 'add_to_cart':
                data['addtocart'] = action['value']
            if action['action_type'] == 'initiate_checkout':
                data['checkout'] = action['value']
        ads.append(data)
    return ads