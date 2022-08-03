import requests
import json
import datetime
# from pprint import pprint
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; POT-AL00 Build/HUAWEIPOT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045709 Mobile Safari/537.36;cplus_app',
    'Accept': 'image/webp,image/tpg,image/*,*/*;q=0.8',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
}

root_url = 'http://pubinfo.sdwcvc.cn'
login_url ='http://pubinfo.sdwcvc.cn/index.jsp'

def login(username, password):
    login_data = json.dumps( {'user_account': username, 'user_password': password})
    s = requests.Session()

    login_reply = s.post(login_url, data=login_data, headers=headers, verify=False)

    login_result = json.loads(login_reply.content)

    if(login_result['code'] != 200):
        print('Login Failed')
        exit()

    s.cookies = login_reply.cookies
    return s
    
def getForm(day, session):
    url = root_url + '/getPunchForm'
    datas = json.dumps({'date': day})
    
    res = session.post(url, data=datas, headers=headers)
    res_json = json.loads(res.content)

    if(res_json['code'] == 200):
        return res_json['datas']
    else:
        return None


def punchForm(form, session):
    url = root_url + '/punchForm'
    date = datetime.datetime.now() + datetime.timedelta(days=1)
    datestr = date.strftime("%Y-%m-%d")
    
    print(datestr)
    
    datas_dict = {
        'punch_form': json.dumps(form),
        'date': datestr
    }
    datas = json.dumps(datas_dict)
    # print(datas)

    res = session.post(url, data=datas, headers=headers)
    res_json = json.loads(res.content)
    print(res_json)


def submit(username, password, address, params=None):
    s = login(username, password)
    # result = s.post(root_url + '/getHomeDate', headers=headers)

    today = datetime.date.today().strftime('%Y-%m-%d')
    form_dict = getForm(today, s)

    fields = form_dict['fields']
    form = { dict['field_code']: dict['user_set_value'] for dict in fields }
    
    for key, value in params.items():
        if not value:
            value = 'null'
        form[key] = value
    
    if address != "":
        form['zddw'] = address

    punchForm(form, s)
