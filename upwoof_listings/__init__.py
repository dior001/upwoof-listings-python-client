api_key = None
url = 'https://www.upwoof.com/api/v1/'
logger = None

def get_client():
    from .client import Client
    if not hasattr(get_client, '_instance'):
        get_client._instance = Client()
    return get_client._instance
