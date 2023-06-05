import shopify
from django.shortcuts import render
from datetime import datetime, timedelta, date
from myapp.s_creds import get_shopify_credentials

def get_shopify_analytics(request):
    account_id = request.GET.get('id')
    # account_name = 'Franke India'
    credentials = get_shopify_credentials(account_id)
    api_key = credentials.get('API_KEY')
    api_secret = credentials.get('API_SECRET')
    access_token = credentials.get('ACCESS_TOKEN')
    shop_url = credentials.get('SHOP_URL')
    api_version = '2023-04'

    shopify.ShopifyResource.set_site(shop_url)
    shopify.Session.setup(api_key=api_key, secret=api_secret)
    session = shopify.Session(shop_url, api_version, access_token)

    shopify.ShopifyResource.activate_session(session)


    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    last_7_days = date.today() - timedelta(days=7)

    # yesterday orders data
    # yesterday_orders = shopify.Order.find(limit=100, status='any', created_at_min=yesterday, created_at_max=today)
    # yesterday_orders_data = []
    # yesterday_customer_order_count = {}
    # yesterday_total_sale = 0
    # yesterday_order_count = 0

    # for order in yesterday_orders:
    #     data = {}
    #     data['id'] = order.id
    #     data['cancel_reason'] = order.cancel_reason
    #     data['cancelled_at'] = order.cancelled_at
    #     data['closed_at'] = order.closed_at
    #     data['created_at'] = order.created_at
    #     data['customer'] = order.customer
    #     data['customer_locale'] = order.customer_locale
    #     data['discount_codes'] = order.discount_codes
    #     data['email'] = order.email
    #     data['financial_status'] = order.financial_status
    #     data['fulfillments'] = order.fulfillments
    #     data['fulfillment_status'] = order.fulfillment_status
    #     data['line_items'] = order.line_items
    #     data['order_number'] = order.order_number
    #     data['payment_gateway_names'] = order.payment_gateway_names
    #     data['processed_at'] = order.processed_at
    #     data['subtotal_price'] = order.subtotal_price
    #     data['total_discounts'] = order.total_discounts
    #     data['total_line_items_price'] = order.total_line_items_price
    #     data['total_price'] = order.total_price
    #     data['total_tax'] = order.total_tax
    #     line_items = []
    #     for line_item in order.line_items:
    #         line_item_data = {
    #             'product_title': line_item.title,
    #             'product_price': line_item.price,
    #             'quantity': line_item.quantity
    #         }
    #         line_items.append(line_item_data)

    #     yesterday_total_sale += float(order.total_price)
    #     yesterday_order_count += int(1)

    #     data['line_items'] = line_items

    #     # Track customer order count
    #     customer_id = order.customer.id
    #     if customer_id in yesterday_customer_order_count:
    #         yesterday_customer_order_count[customer_id] += 1
    #     else:
    #         yesterday_customer_order_count[customer_id] = 1

    #     yesterday_orders_data.append(data)

    # yesterday_average_order_value = round(float(yesterday_total_sale) / int(yesterday_order_count), 2)

    # last 7 days data
    last_7_days_orders = shopify.Order.find(limit=250, status='any', created_at_min=last_7_days, created_at_max=today)
    last_7_days_orders_data = []
    last_7_days_customer_order_count = {}
    product_quantity = {}
    last_7_days_total_sale = 0
    last_7_days_total_order = 0
    last_7_days_nc = 0

    for order in last_7_days_orders:
        data = {}
        last_7_days_total_sale += float(order.total_price)
        last_7_days_total_order += 1

        # print(order.customer.attributes.get('orders_count'))
        # print(order.attributes)
        # print(order.customer.attributes)

        line_items = order.line_items

        for line_item in line_items:
            product_title = line_item.title
            quantity = line_item.quantity
            price = line_item.price

            if product_title in product_quantity:
                product_quantity[product_title]['total_quantity'] += quantity
            else:
                product_quantity[product_title] = {
                    'total_quantity': quantity,
                    'price': price
                }

        # Track customer order count
        customer_id = order.customer.id
        if customer_id in last_7_days_customer_order_count:
            last_7_days_customer_order_count[customer_id] += 1
        else:
            last_7_days_customer_order_count[customer_id] = 1

        last_7_days_orders_data.append(data)

    for id, count in last_7_days_customer_order_count.items():
        if count == 1:
            last_7_days_nc += 1

    # Retrieve top selling products
    top_selling_product = []
    for product_title, item_data in product_quantity.items():
        top_selling_product.append({
            'product_title': product_title,
            'total_quantity': item_data['total_quantity'],
            'price': item_data['price'],
            'gross': round(float(item_data['price']) * int(item_data['total_quantity']),2)
        })

    top_selling_product = sorted(top_selling_product, key=lambda x: x['gross'], reverse=True)
    last_7_days_aov = round(float(last_7_days_total_sale)/int(last_7_days_total_order),2)

    # print(last_7_days_orders_data)

    shopify.ShopifyResource.clear_session()

    return render(request, 'myapp/shopify/index.html', {
        # 'yesterday_orders_data': yesterday_orders_data,
        # 'yesterday_customer_order_count': yesterday_customer_order_count,  
        # 'yesterday_total_sale': yesterday_total_sale,
        # 'yesterday_order_count' : yesterday_order_count,
        # 'yesterday_average_order_value': yesterday_average_order_value,
        # 'last_7_days_orders_data': last_7_days_orders_data,
        # 'last_7_days_customer_order_count': last_7_days_customer_order_count,
        'top_selling_product': top_selling_product, 
        'last_7_days_total_order': last_7_days_total_order,
        'last_7_days_total_sale': last_7_days_total_sale,
        'last_7_days_aov': last_7_days_aov,
        'last_7_days_nc': last_7_days_nc,
    })

