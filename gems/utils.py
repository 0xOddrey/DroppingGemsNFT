from .models import TwitterToken, twitterConnection
from requests import post, put, get

def get_user_tokens(session_id):
    user_tokens=TwitterToken.objects.filter(session_id=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else: 
        return None 

def update_or_create_user_token(session_id, oauth_token, oauth_secret, user_id, user_name):
    tokens = get_user_tokens(session_id)
    if tokens:
        tokens.oauth_token=oauth_token
        tokens.oauth_secret=oauth_secret
        tokens.user_id=user_id
        tokens.user_name=user_name 
        try:
            tokens.save(update_fields=['oauth_token',
            'oauth_secret', 'user_id','user_name'], force_update=True)
        except Exception as e:
            print(e)
    else:
        tokens = TwitterToken(session_id=session_id, oauth_token=oauth_token,
        oauth_secret=oauth_secret, user_id=user_id, user_name=user_name)
        try:
            tokens.save(force_insert=True)
        except Exception as e:
            print(e)
    
def is_twitter_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        return True 
    else: return False 