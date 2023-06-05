from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.conf import settings
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet

app_id = '753892059567274'
app_secret = '7c890c7737505893c176aeef85fb5739'
access_token = 'EAAKtqSxo1KoBAGFWIfZC7esGLxgEnyLpnNJGSiMrwpRFZBV9vTNJAEcKYRHGHP35kaw01PSw0whBMiiM2eiwnSNWNH4OrOyqPRYQuPqmyfwi94YRiILKkHi8Vrz5SNm71z4KpmvoTEoBTtT7BnXi1SN6IxHVhCVp5YqHnY02wNyWmOZA175diE77fYvOROgcPPJWjmiPbZCOWWk3wy0Prdq0GfjL3y4nrTOlHA5PBmbCwRsDjTT7'
account_id = "act_504617430378007"

def ad_data(request):
    FacebookAdsApi.init(app_id, app_secret, access_token)
    ad_account = AdAccount(account_id)
    campaigns = ad_account.get_campaigns(fields=['name', 'objective', 'status'])
    return render(request, 'myapp/ad_data.html', {'campaigns': campaigns})


def campaign_insights(request):
    FacebookAdsApi.init(app_id, app_secret, access_token)
    account = AdAccount(account_id)
    fields = [
        'account_id',
        'campaign_id',
        'campaign_name',
        'clicks',
        'impressions',
        'spend',
        'reach',
        'frequency',
        'ctr',
        'cpm',
        'cpp',
        'cpc',
        'objective',
        'inline_link_click_ctr',
        'actions',
    ]
    params = {'time_range': {'since':'2023-04-21','until':'2023-04-21'}, 'level': 'campaign'}
    insights = account.get_insights(fields=fields, params=params)
    campaigns = []
    for insight in insights:
        campaign = {}
        campaign['accountid'] = insight['account_id']
        campaign['id'] = insight['campaign_id']
        campaign['name'] = insight['campaign_name']
        campaign['clicks'] = insight['clicks']
        campaign['impressions'] = insight['impressions']
        campaign['spend'] = insight['spend']
        campaign['actions'] = insight['actions']
        # campaign['reach'] = insight['reach']
        # campaign['frequency'] = insight['frequency']
        # campaign['ctr'] = insight['ctr']
        # campaign['cpm'] = insight['cpm']
        # campaign['cpp'] = insight['cpp']
        # campaign['cpc'] = insight['cpc']
        # campaign['objective'] = insight['objective']
        # campaign['inlineClick'] = insight['inline_link_click_ctr']
        campaigns.append(campaign)

    return render(request, 'myapp/campaign_insights.html', {'campaigns': campaigns})

def calculate_delta(num1, num2):
    result = round((((num1-num2)/num2)*100),4)
    return result

def account_data(request):
    FacebookAdsApi.init(app_id,app_secret,access_token)
    account = AdAccount(account_id)

    today = date.today() - timedelta(days=1)
    yesterday = date.today() - timedelta(days=1)
    last_7_days = date.today() - timedelta(days=7)
    month_start = datetime.now().replace(day=1).date()

    yesterday_delta = date.today() - timedelta(days=2)
    last_7_days_delta = date.today() - timedelta(days=14)
    month_start_delta_last_date = month_start - timedelta(days=1)
    month_start_delta = month_start_delta_last_date.replace(day=1)

    fields = [
        AdsInsights.Field.clicks,
        AdsInsights.Field.actions,
        AdsInsights.Field.impressions,
        AdsInsights.Field.spend,
    ]

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
    month_start_insights = account.get_insights(
        fields=fields,
        params={
            'time_range': {
                'since': str(today),
                'until': str(month_start),
            },
            'level': 'account',
        }
    )
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
    month_start_delta_insights = account.get_insights(
        fields=fields,
        params={
            'time_range': {
                'since': str(month_start_delta),
                'until': str(month_start_delta_last_date),
            },
            'level': 'account',
        }
    )

    yesterday_data = yesterday_insights[0]
    last_7_days_data = last_7_days_insights[0]
    month_start_data = month_start_insights[0]

    yesterday_delta_data = yesterday_delta_insights[0]
    last_7_days_delta_data = last_7_days_delta_insights[0]
    month_start_delta_data = month_start_delta_insights[0]

    yesterday_result = {
        'clicks': yesterday_data.get('clicks', 0),
        'actions': yesterday_data.get('actions', 0),
        'impressions': yesterday_data.get('impressions', 0),
        'spend': yesterday_data.get('spend', 0),
    }
    for action in yesterday_result['actions']:
        if action['action_type'] == 'leadgen_grouped':
            yesterday_result['result'] = action['value']
            break

    last_7_days_result = {
        'clicks': last_7_days_data.get('clicks', 0),
        'actions': last_7_days_data.get('actions', 0),
        'impressions': last_7_days_data.get('impressions', 0),
        'spend': last_7_days_data.get('spend', 0),
    }
    for action in last_7_days_result['actions']:
        if action['action_type'] == 'leadgen_grouped':
            last_7_days_result['result'] = action['value']
            break

    month_start_result = {
        'clicks': month_start_data.get('clicks', 0),
        'actions': month_start_data.get('actions', 0),
        'impressions': month_start_data.get('impressions', 0),
        'spend': month_start_data.get('spend', 0),
    }
    for action in month_start_result['actions']:
        if action['action_type'] == 'leadgen_grouped':
            month_start_result['result'] = action['value']
            break

    # delta data
    yesterday_delta_result = {
        'clicks': calculate_delta(int(yesterday_data.get('clicks', 0)), int(yesterday_delta_data.get('clicks', 0))),
        'actions': yesterday_delta_data.get('actions', 0),
        'impressions': calculate_delta(int(yesterday_data.get('impressions', 0)), int(yesterday_delta_data.get('impressions', 0))),
        'spend': calculate_delta(float(yesterday_data.get('spend', 0)) , float(yesterday_delta_data.get('spend', 0))),
    }
    for action in yesterday_delta_result['actions']:
        if action['action_type'] == 'leadgen_grouped':
            yesterday_delta_result['result'] = calculate_delta(int(yesterday_result['result']), int(action['value']))
            break

    last_7_days_delta_result = {
        'clicks': calculate_delta(int(last_7_days_data.get('clicks', 0)), int(last_7_days_delta_data.get('clicks', 0))),
        'actions': last_7_days_delta_data.get('actions', 0),
        'impressions': calculate_delta(int(last_7_days_data.get('impressions', 0)), int(last_7_days_delta_data.get('impressions', 0))),
        'spend': calculate_delta(float(last_7_days_delta_data.get('spend', 0)), float(last_7_days_delta_data.get('spend', 0))),
    }
    for action in last_7_days_delta_result['actions']:
        if action['action_type'] == 'leadgen_grouped':
            last_7_days_delta_result['result'] = calculate_delta(int(last_7_days_result['result']), int(action['value']))
            break

    month_start_delta_result = {
        'clicks': calculate_delta(int(month_start_data.get('clicks', 0)), int(month_start_delta_data.get('clicks', 0))),
        'actions': month_start_delta_data.get('actions', 0),
        'impressions': calculate_delta(int(month_start_data.get('impressions', 0)), int(month_start_delta_data.get('impressions', 0))),
        'spend': calculate_delta(float(month_start_data.get('spend', 0)), float(month_start_delta_data.get('spend', 0))),
    }
    for action in month_start_delta_result['actions']:
        if action['action_type'] == 'leadgen_grouped':
            month_start_delta_result['result'] = calculate_delta(int(month_start_result['result']), int(action['value']))
            break


    return render(request, 'myapp/old_account.html',{
        'yesterday': yesterday_result,
        'last_7_days': last_7_days_result,
        'month_start': month_start_result,
        'yesterday_delta': yesterday_delta_result,
        'last_7_days_delta': last_7_days_delta_result,
        'month_start_delta': month_start_delta_result,
    })

def account(request):
    FacebookAdsApi.init(app_id,app_secret,access_token)
    account = AdAccount("act_513018249125789")

    fields = [
       'account_name',
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

    breakdowns = ['age']

    today = date.today() - timedelta(days=1)
    yesterday = date.today() - timedelta(days=1)
    last_3_days = date.today() - timedelta(days=3)
    last_7_days = date.today() - timedelta(days=7)
    last_30_days = date.today() - timedelta(days=30)

    yesterday_insights = account.get_insights(
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

    last_3_days_insights = account.get_insights(
        fields=fields,
        params={
            'time_range': {
                'since': str(last_3_days),
                'until': str(today),
            },
            'level': 'account',
            'breakdowns': breakdowns,
        }
    )

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

    yesterday_data = yesterday_insights[0]
    last_3_days_data = last_3_days_insights[0]
    last_7_days_data = last_7_days_insights[0]
    last_30_days_data = last_30_days_insights[0]

    # for insights in last_3_days_insights:
    #     print(insights)

    yesterday_result = {
        'account_name': yesterday_data.get('account_name',''),
        'spend': yesterday_data.get('spend', 0),
        'cpm': yesterday_data.get('cpm', 0),
        'impressions': yesterday_data.get('impressions', 0),
        'actions': yesterday_data.get('actions', 0),
        'reach': yesterday_data.get('reach', 0),
        'purchase_roas': yesterday_data.get('purchase_roas', 0),
        'frequency': yesterday_data.get('frequency', 0),
        'cpc': yesterday_data.get('cpc', 0),
        'cost_per_inline_link_click': yesterday_data.get('cost_per_inline_link_click', 0),
        'ctr': yesterday_data.get('ctr', 0),
        'breakdowns': yesterday_data.get('breakdowns', 0),
        'outbound_clicks_ctr': yesterday_data.get('outbound_clicks_ctr', 0),
    }
    for action in yesterday_result['actions']:
        if action['action_type'] == 'purchase':
            yesterday_result['result'] = action['value']
            break

    last_3_days_result = {
        'account_name': last_3_days_data.get('account_name',''),
        'spend': last_3_days_data.get('spend', 0),
        'cpm': last_3_days_data.get('cpm', 0),
        'impressions': last_3_days_data.get('impressions', 0),
        'actions': last_3_days_data.get('actions', 0),
        'reach': last_3_days_data.get('reach', 0),
        'purchase_roas': last_3_days_data.get('purchase_roas', 0)[0]["value"],
        'frequency': last_3_days_data.get('frequency', 0),
        'cpc': last_3_days_data.get('cpc', 0),
        'cost_per_inline_link_click': last_3_days_data.get('cost_per_inline_link_click', 0),
        'ctr': last_3_days_data.get('ctr', 0),
        'outbound_clicks_ctr': last_3_days_data.get('outbound_clicks_ctr', 0)[0]["value"],
    }
    for action in last_3_days_result['actions']:
        if action['action_type'] == 'purchase':
            last_3_days_result['result'] = action['value']
            break

    last_7_days_result = {
        'account_name': last_7_days_data.get('account_name',''),
        'spend': last_7_days_data.get('spend', 0),
        'cpm': last_7_days_data.get('cpm', 0),
        'impressions': last_7_days_data.get('impressions', 0),
        'actions': last_7_days_data.get('actions', 0),
        'reach': last_7_days_data.get('reach', 0),
        'purchase_roas': last_7_days_data.get('purchase_roas', 0)[0]["value"],
        'frequency': last_7_days_data.get('frequency', 0),
        'cpc': last_7_days_data.get('cpc', 0),
        'cost_per_inline_link_click': last_7_days_data.get('cost_per_inline_link_click', 0),
        'ctr': last_7_days_data.get('ctr', 0),
        'outbound_clicks_ctr': last_7_days_data.get('outbound_clicks_ctr', 0)[0]["value"],
    }
    for action in last_7_days_result['actions']:
        if action['action_type'] == 'purchase':
            last_7_days_result['result'] = action['value']
            break

    last_30_days_result = {
        'account_name': last_30_days_data.get('account_name',''),
        'spend': last_30_days_data.get('spend', 0),
        'cpm': last_30_days_data.get('cpm', 0),
        'impressions': last_30_days_data.get('impressions', 0),
        'actions': last_30_days_data.get('actions', 0),
        'reach': last_30_days_data.get('reach', 0),
        'purchase_roas': last_30_days_data.get('purchase_roas', 0)[0]["value"],
        'frequency': last_30_days_data.get('frequency', 0),
        'cpc': last_30_days_data.get('cpc', 0),
        'cost_per_inline_link_click': last_30_days_data.get('cost_per_inline_link_click', 0),
        'ctr': last_30_days_data.get('ctr', 0),
        'outbound_clicks_ctr': last_30_days_data.get('outbound_clicks_ctr', 0)[0]["value"],
    }
    for action in last_30_days_result['actions']:
        if action['action_type'] == 'purchase':
            last_30_days_result['result'] = action['value']
            break

    return render(request, 'myapp/account.html',{
        'yesterday': yesterday_result,
        'last_3_days': last_3_days_result,
        'last_7_days': last_7_days_result,
        'last_30_days': last_30_days_result,
    })