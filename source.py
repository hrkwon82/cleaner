import re
import requests
import json
import time
import random
import js2py
import threading
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

print ("HS클리너 ver1.8")
print ("\n")

def process(user_id,user_pw):

    decode_service_code='''
    function get_service_code(service_code, r_value){

        var a,e,n,t,f,d,h,i = "yL/M=zNa0bcPQdReSfTgUhViWjXkYIZmnpo+qArOBs1Ct2D3uE4Fv5G6wHl78xJ9K",
        o = "",
        c = 0;
        for (r_value = r_value.replace(/[^A-Za-z0-9+/=]/g,""); c < r_value.length;) {
            t = i.indexOf(r_value.charAt(c++));
            f = i.indexOf(r_value.charAt(c++));
            d = i.indexOf(r_value.charAt(c++));
            h = i.indexOf(r_value.charAt(c++));
            a = t << 2 | f >> 4;
            e = (15 & f) << 4 | d >> 2;
            n = (3 & d) << 6 | h;
            o += String.fromCharCode(a);
            64 != d && (o += String.fromCharCode(e));
            64 != h && (o += String.fromCharCode(n));
        }
        var tvl = o;
        var fi = parseInt(tvl.substr(0,1));
        fi = fi > 5 ? fi - 5 : fi + 4;
        var _r = tvl.replace(/^./, fi);
        var _rs = _r.split(",");
        var replace = "";
        for (e = 0; e < _rs.length; e++) replace += String.fromCharCode(2 * (_rs[e] - e - 1) / (13 - e - 1));
        return service_code.replace(/(.{10})$/, replace)
    }
    '''

    decode_service_code = js2py.eval_js(decode_service_code)

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

    req = session.get('https://gallog.dcinside.com/%s/posting'%user_id)
    soup = BeautifulSoup(req.text,'lxml')

    service_code_origin = soup.find('input', {'name' : 'service_code'})['value']
    ci_t = session.cookies.get_dict()['ci_c']

    data  = soup.select("script")[29]

    cut_1 = "var _r = _d"
    cut_2 = '<script type="text/javascript">'
    cut_3 = "</script>"

    cut_data = str(data).replace(cut_1,"")
    cut_data = str(cut_data).replace(cut_2,"")
    cut_data = str(cut_data).replace(cut_3,"")
    _r = re.sub("\n","",str(cut_data))
    r_value = re.sub("['();]","",str(_r))
    r_value = str(r_value)
    # 정규식

    service_code = decode_service_code(service_code_origin, r_value)

    print ("\n")
    print ("service_code_origin -> "+ service_code_origin)
    print ("\n")
    
    print (r_value)

    print ("\n")
    print ("service_code -> "+ service_code)
    print ("\n")

    time.sleep(5)

    while True: #post delete

        req = session.get('https://gallog.dcinside.com/%s/posting'%user_id)
        soup = BeautifulSoup(req.text,'lxml')
        content_form = soup.select('ul.cont_listbox > li')
        print ("LOAD")

        if not content_form:
            print ("더이상 삭제할 게시글이 없어요!")
            break
        else:
            pass

        delete_set = []

        for i in content_form:
            data_no = (i.attrs['data-no'])
            delete_set.append(data_no)

        for set in delete_set:
        

            delete_data = {
                "ci_t" : ci_t,
                "no" : set,
                "service_code" : service_code
            }

            time.sleep(0.5)
            req = session.post('https://gallog.dcinside.com/%s/ajax/log_list_ajax/delete'%user_id,data=delete_data)

            result = req.text
            print ("posting -> " + set + " -> " + result)
            
        delete_set.clear()

    while True: #comment delete

        req = session.get('https://gallog.dcinside.com/%s/comment'%user_id)
        soup = BeautifulSoup(req.text,'lxml')
        content_form = soup.select('ul.cont_listbox > li')
        print ("LOAD")

        if not content_form:
            print ("더이상 삭제할 댓글이 없어요!")
            break
        else:
            pass

        delete_set = []

        for i in content_form:
            data_no = (i.attrs['data-no'])
            delete_set.append(data_no)

        for set in delete_set:
        

            delete_data = {
                "ci_t" : ci_t,
                "no" : set,
                "service_code" : service_code
            }

            time.sleep(0.5)
            req = session.post('https://gallog.dcinside.com/%s/ajax/log_list_ajax/delete'%user_id,data=delete_data)

            result = req.text
            print ("comment -> " + set + " -> " + result)

    print ("\n")
    input ("클리너 작동을 마쳤어요! : ") #press any key


if __name__ == "__main__": 
    
    usid = input("ID : ")
    uspw = input("PW : ")
    process(usid,uspw)