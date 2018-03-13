import requests


class Yunpian():

    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_url = 'xxx.com'

    def send_sms(self,code,mobile):
        parmas = {
            'apikey':self.api_key,
            'mobile':mobile,
            'text':'xxxx{code}'.format(code=code)
        }
        response = requests.post(self.single_send_url,data=parmas)
        import json
        re_dict = json.loads(response.text)
        print(re_dict)

if __name__=="__main__":
    yunpian = Yunpian('xxxxxx')
    yunpian.send_sms('2018','13121122211')