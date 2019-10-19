# 2019-9-17

import requests
import re
import time
from bs4 import BeautifulSoup
from decode_py import decode

def del_pos(SESS,DEL_FLAG,user_id):

        req = SESS.get('https://gallog.dcinside.com/%s/posting'%user_id)
        soup = BeautifulSoup(req.text,'lxml')

        service_code_origin = soup.find('input', {'name' : 'service_code'})['value']

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

        service_code = decode(service_code_origin, r_value)

        time.sleep(0.5)

        while True: #P_DEL

            try:

                req = SESS.get('https://gallog.dcinside.com/%s/posting'%user_id)
                soup = BeautifulSoup(req.text,'lxml')
                content_form = soup.select('ul.cont_listbox > li')
                print ("LOAD")

                if not content_form:
                    DEL_FLAG.append('True')
                    break
                else:
                    pass

                delete_set = []

                for i in content_form:
                    data_no = (i.attrs['data-no'])
                    delete_set.append(data_no)

                for set in delete_set:
                        
                    delete_data = {
                        "no" : set,
                        "service_code" : service_code
                    }

                    time.sleep(0.5)
                    req = SESS.post('https://gallog.dcinside.com/%s/ajax/log_list_ajax/delete'%user_id,data=delete_data)

                    result = req.text
                            
                delete_set.clear()
                    
            except Exception as ex:
                print (ex)
                pass
