
def get_auth_url():
    weibo_auth_url = 'http://api.weibo.com/oauth2/authorize'
    redirect_url = ''
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_url={re_url}".format(client_id=1111,re_re_url=redirect_url)
    print(auth_url)


def get_access_token(code='xxx'):
    access_token_url = 'http://api.weibo.com/oauth2/access_token'
    import requests
    re_dict = requests.post(access_token_url,data={
        'client_id':"",
        'client_secret':'',
        'grant_type':'authorization',
        'code':code,
        'redirect_url':'',
    })