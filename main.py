from dotenv import load_dotenv
import os
from crawlQuestion import *
from genAnswer import *
from saveWord import *
from toTXT import *

load_dotenv()

if __name__ == '__main__':
    link_page = 'https://trangnguyen.edu.vn/dang-nhap'
    list_account = os.environ.get("ACCOUNT").split(',')
    list_password = os.environ.get("PASSWORD").split(',')
    
    index = 1
    for account, password in zip(list_account, list_password):
        # if index == 1:
        #     index += 1
        #     continue
        
        path_folder = 'Khoi ' + str(index)
        main_crawl_question(link_page, account, password, path_folder)
        main_to_TXT(path_folder)
        main_gen_answer(path_folder)
        main_save_word(path_folder)

        index += 1
    
    print("XONG")