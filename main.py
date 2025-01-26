from crawlQuestion import *
from genAnswer import *
from saveWord import *
from toTXT import *

if __name__ == '__main__':
    path_folder = 'Khoi 4'

    link_page = 'https://trangnguyen.edu.vn/dang-nhap'
    account = 'z1khoi4'
    password = 'Dieu@Dieu@#$234'

    main_crawl_question(link_page, account, password, path_folder)
    main_to_TXT(path_folder)
    main_gen_answer(path_folder)
    main_save_word(path_folder)