from django.shortcuts import render, redirect
from facebook_business.api import FacebookAdsApi

def get_facebook_access_token(request):
    # Replace these values with your own Facebook App ID and App Secret
    app_id = '980051950029276'
    app_secret = 'a0e810998ea35b9f738c5b8ab2efab23'

    # If the user is not already authenticated with Facebook, redirect them to the login page
    if not request.GET.get('code'):
        redirect_uri = request.build_absolute_uri(request.path)
        scope = 'ads_management,ads_read,business_management'
        redirect_url = 'https://www.facebook.com/v16.0/dialog/oauth?client_id={}&redirect_uri={}&scope={}'.format(
            app_id, redirect_uri, scope
        )
        return redirect(redirect_url)

    # If the user has been redirected back from Facebook after logging in, exchange the temporary code for an access token
    code = request.GET.get('code')
    try:
        access_token = FacebookAdsApi.get_default_api().get_access_token_from_code(
            code, request.build_absolute_uri(request.path), app_id, app_secret
        )
    except Exception as e:
        # Handle any errors that occur during the access token exchange
        return render(request, 'myapp/facebook/home.html', {'error': str(e)})

    # If access_token is None, return an error message
    if access_token is None:
        return render(request, 'myapp/facebook/home.html', {'error': 'Failed to retrieve access token from Facebook.'})

    # Return the access token
    return render(request, 'myapp/facebook/home.html', {'access_token': access_token})

