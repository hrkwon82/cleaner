# 2019-9-20

import requests
import re
import time
from bs4 import BeautifulSoup

def del_pos(SESS,DEL_FLAG,user_id,service_code):

        print ("asdf")

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
                    req = SESS.post('https://gallog.dcinside.com/%s/ajax/log_list_ajax/delete'%user_id,data=delete_data,timeout=10)
                    result = req.text
                    print (result)
                            
                delete_set.clear()
                    
            except Exception as ex:
                print (ex)
                pass
