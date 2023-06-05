from django.shortcuts import render
from datetime import datetime, timedelta, date
from django.conf import settings
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adaccount import AdAccount
from myapp.s_creds import get_shopify_credentials
import json
from dotenv import load_dotenv
import os
from myapp.functions import get_yesterday_regular_metrix, get_last_3_days_regular_metrix, get_last_7_days_regular_metrix, get_last_30_days_regular_metrix, get_yesterday_delta_metrix, get_last_3_days_delta_metrix, get_last_7_days_delta_metrix, get_last_30_days_delta_metrix, get_yesterday_regular_metrix_campaigns, get_last_3_days_regular_metrix_campaigns, get_last_7_days_regular_metrix_campaigns, get_last_30_days_regular_metrix_campaigns, get_yesterday_delta_metrix_campaigns, get_last_3_days_delta_metrix_campaigns, get_last_7_days_delta_metrix_campaigns, get_last_30_days_delta_metrix_campaigns, get_yesterday_regular_metrix_adsets, get_last_3_days_regular_metrix_adsets, get_last_7_days_regular_metrix_adsets, get_last_30_days_regular_metrix_adsets, get_yesterday_delta_metrix_adsets, get_last_3_days_delta_metrix_adsets, get_last_7_days_delta_metrix_adsets, get_last_30_days_delta_metrix_adsets, get_yesterday_regular_metrix_ads, get_last_3_days_regular_metrix_ads, get_last_7_days_regular_metrix_ads, get_last_30_days_regular_metrix_ads, get_yesterday_delta_metrix_ads, get_last_3_days_delta_metrix_ads, get_last_7_days_delta_metrix_ads, get_last_30_days_delta_metrix_ads

load_dotenv()

# active account list
active_accounts = ["act_201787132", "act_173956531555350", "act_205726624613379", "act_226379489336447", "act_264068678811945", "act_278716730753634", "act_329062928187663", "act_340111427307697", "act_417890117196109", "act_504617430378007", "act_513018249125789", "act_527728824624183", "act_569932057220010", "act_572685291325737", "act_744689400566478", "act_782337812306907", "act_896151067748583", "act_910210063093210", "act_912179029316314", "act_1098366407319169", "act_1135260870511791", "act_1237099966710816", "act_1511612239319160", "act_1817273581872129", "act_2809922719048506", "act_3973595269347261", "act_5659554837438767"]


# def fetch_and_write_data():
#     FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
#     # business = Business(fbid=os.environ['BUSINESS_ID'])

#     # getting list of all account in bussiness account
#     fields = [
#         'account_name',
#         'account_id',
#     ]

#     # ad_accounts = business.api_get(fields=['name']).get_client_ad_accounts(fields=fields)
#     ad_account_list =[]
#     ad_account_info={}

#     for id in active_accounts:
#         account = AdAccount(str(id))
#         response = account.get_insights(fields=fields)
#         account_data = response[0]
#         ad_account_info = {
#             'account_id': 'act_'+account_data.get('account_id'),
#             'account_name': account_data.get('account_name'),
#             'shopify': 0
#         }
#         data = get_shopify_credentials(account_data.get('account_id'))
#         if data:
#             ad_account_info['shopify'] = 1
#             ad_account_info['s_id'] = account_data.get('account_id')
#         ad_account_info['yesterday_result'] = get_yesterday_regular_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['last_3_days_result'] = get_last_3_days_regular_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['last_7_days_result'] = get_last_7_days_regular_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['last_30_days_result'] = get_last_30_days_regular_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['yesterday_delta_result'] = get_yesterday_delta_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['last_3_days_delta_result'] = get_last_3_days_delta_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['last_7_days_delta_result'] = get_last_7_days_delta_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['last_30_days_delta_result'] = get_last_30_days_delta_metrix('act_'+account_data.get('account_id'))
#         ad_account_info['yesterday_campaigns_result'] = get_yesterday_regular_metrix_campaigns('act_'+account_data.get('account_id'))
#         ad_account_info['last_3_days_campaigns_result'] = get_last_3_days_regular_metrix_campaigns('act_'+account_data.get('account_id'))
#         ad_account_info['last_7_days_campaigns_result'] = get_last_7_days_regular_metrix_campaigns('act_'+account_data.get('account_id'))
#         ad_account_info['last_30_days_campaigns_result'] = get_last_30_days_regular_metrix_campaigns('act_'+account_data.get('account_id'))
        # ad_account_info['yesterday_campaigns_delta_result'] = get_yesterday_delta_metrix_campaigns('act_'+account_data.get('account_id'))
        # ad_account_info['last_3_days_campaigns_delta_result'] = get_last_3_days_delta_metrix_campaigns('act_'+account_data.get('account_id'))
        # ad_account_info['last_7_days_campaigns_delta_result'] = get_last_7_days_delta_metrix_campaigns('act_'+account_data.get('account_id'))
        # ad_account_info['last_30_days_campaigns_delta_result'] = get_last_30_days_delta_metrix_campaigns('act_'+account_data.get('account_id'))
        # ad_account_info['yesterday_adsets_result'] = get_yesterday_regular_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['last_3_days_adsets_result'] = get_last_3_days_regular_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['last_7_days_adsets_result'] = get_last_7_days_regular_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['last_30_days_adsets_result'] = get_last_30_days_regular_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['yesterday_adsets_delta_result'] = get_yesterday_delta_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['last_3_days_adsets_delta_result'] = get_last_3_days_delta_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['last_7_days_adsets_delta_result'] = get_last_7_days_delta_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['last_30_days_adsets_delta_result'] = get_last_30_days_delta_metrix_adsets('act_'+account_data.get('account_id'))
        # ad_account_info['yesterday_ads_result'] = get_yesterday_regular_metrix_ads('act_'+account_data.get('account_id'))
        # ad_account_info['last_3_days_ads_result'] = get_last_3_days_regular_metrix_ads('act_'+account_data.get('account_id'))
        # ad_account_info['last_7_days_ads_result'] = get_last_7_days_regular_metrix_ads('act_'+account_data.get('account_id'))
        # ad_account_info['last_30_days_ads_result'] = get_last_30_days_regular_metrix_ads('act_'+account_data.get('account_id'))
        # ad_account_info['yesterday_ads_delta_result'] = get_yesterday_delta_metrix_ads('act_'+account_data.get('account_id'))
        # ad_account_info['last_3_days_ads_delta_result'] = get_last_3_days_delta_metrix_ads('act_'+account_data.get('account_id'))
        # ad_account_info['last_7_days_ads_delta_result'] = get_last_7_days_delta_metrix_ads('act_'+account_data.get('account_id'))
        # ad_account_info['last_30_days_ads_delta_result'] = get_last_30_days_delta_metrix_ads('act_'+account_data.get('account_id'))
#         ad_account_list.append(ad_account_info)

#     current_directory = os.getcwd()
#     file_path = os.path.join(current_directory, 'data.json')

#     print("Before writing to file")
#     with open(file_path, 'w') as file:
#         json.dump(ad_account_list, file)
#     print("After writing to file")



# fetch_and_write_data()






def get_all_accounts(request):

    FacebookAdsApi.init(os.environ['APP_ID'],os.environ['APP_SECRET'],os.environ['ACCESS_TOKEN'])
    business = Business(fbid=os.environ['BUSINESS_ID'])
    
    # getting list of all account in bussiness account
    fields = [
        AdAccount.Field.id,
        AdAccount.Field.name,
        AdAccount.Field.account_status,
    ]

    ad_accounts = business.api_get(fields=['name']).get_client_ad_accounts(fields=fields)
    ad_account_list =[]

    for ad_account in ad_accounts:
        if ad_account['account_status'] == 1:
            ad_account_info = {
                'id': ad_account['id'],
                'name': ad_account['name'],
                'account_status': ad_account['account_status'],
                'shopify': 0
            }
            data = get_shopify_credentials(ad_account['id'])
            if data:
                ad_account_info['shopify'] = 1
                ad_account_info['s_id'] = ad_account['id']
            ad_account_list.append(ad_account_info)

    
    return render(request, 'myapp/facebook/index.html',{
        'account_list' : ad_account_list,
    })