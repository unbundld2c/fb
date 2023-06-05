SHOP_CREDENTIALS = {
    'act_1135260870511791': {
        'NAME' : 'Franke India',
        'API_KEY': '1a5c4b5d50f1048b75c5173792096651',
        'API_SECRET': '33775e3759305451cb981616060b4db9',
        'ACCESS_TOKEN': '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',
        'SHOP_URL': 'https://faber-india.myshopify.com'
    },
}

def get_shopify_credentials(account_id):
    return SHOP_CREDENTIALS.get(account_id, {})
