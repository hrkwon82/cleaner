# 2019-9-17

import requests
from bs4 import BeautifulSoup

def login(user_id,user_pw):
    
    session = requests.session()

    session.headers = { #session.headers -> Login Referer
        #header..
        'X-Requested-With' : 'XMLHttpRequest',
        'Referer': 'https://www.dcinside.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    soup = BeautifulSoup(session.get("https://www.dcinside.com/").text, features='lxml')
    loginForm = soup.find('form', attrs={'id' : 'login_process'})
    Lauth = loginForm.find_all('input', attrs={'type':'hidden'})[2]

    login_data = {
        "user_id" : user_id,
        "pw" : user_pw,
        "s_url" : "https://www.dcinside.com/",
        "ssl" : "Y",
        Lauth['name']:Lauth['value']
    }

    req = session.post('https://dcid.dcinside.com/join/member_check.php',data=login_data)
            
    session.headers = { #session.headers -> Gallog Referer
        #header..
        'X-Requested-With' : 'XMLHttpRequest',
        'Referer': 'https://gallog.dcinside.com/%s/posting'%user_id,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    if 'history.back(-1);' in req.text:
        return 0
    else:
        SESS = session
        return SESS