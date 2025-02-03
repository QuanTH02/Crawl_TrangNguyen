import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib3
import os
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # Tắt log không cần thiết
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Tắt log lỗi của Chrome
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

driver = webdriver.Chrome(options=chrome_options)

def clean_folder_name(folder_name):
    invalid_chars = ['?', '*', ':', '"', '<', '>', '|', '/', '.', ',']
    for char in invalid_chars:
        folder_name = folder_name.replace(char, '')
    return folder_name

def clean_file_name(file_name):
    invalid_chars = ['?', '*', ':', '"', '<', '>', '|', '/', '.', ',']
    for char in invalid_chars:
        file_name = file_name.replace(char, '')
    return file_name[:55]

def login(page_main_url, account, password):
    # driver.maximize_window()
    driver.get(page_main_url)
    time.sleep(1)

    username_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/form/div[1]/div/input')
    password_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/form/div[2]/div/input')

    username_input.send_keys(account)
    password_input.send_keys(password)
    time.sleep(1)

    login_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/form/button')
    login_button.click()
    time.sleep(1)

# Tạo thư mục
def mkdir(pathFile):
    if not os.path.exists(pathFile):
        os.mkdir(pathFile)

# Chuyển outerHTML thành soup để xử lý các câu hỏi
def outerHTMLtoSoup(outerHTML, thumuccon):
    soup = BeautifulSoup(outerHTML, 'html.parser')

    # Loại bỏ tất cả các thẻ input radio
    radio_inputs = soup.find_all('input', {'type': 'radio'})
    for radio in radio_inputs:
        radio.decompose()

    # Thêm ký hiệu [[ ]] cho các input elements rồi xóa chúng
    input_elements = soup.find_all('input')
    for input_element in input_elements:
        input_element.insert_before('[[]]')
        input_element.decompose()

    # Xử lý các câu hỏi trong thẻ <p> với class cụ thể
    question_elements = soup.find_all('p', class_='text-base font-bold md:text-xl')
    for question in question_elements:
        question_number = question.text.strip().split()[-1]
        question.replace_with(f'Câu {question_number}.')

    # Xử lý các thẻ img
    img_elements = soup.find_all('img')
    for img in img_elements:
        img_url = img.get('src')
        if img_url:
            if img.get('alt') == 'Loa':
                img.replace_with('((Audio))')
            else:
                img.replace_with(f'Image: {img_url}')

    # Xử lý các thẻ video
    video_elements = soup.find_all('video')
    for video in video_elements:
        video.replace_with('((Video)): ' + thumuccon)

    # Thêm đoạn văn bản "Dưới đây là các nhóm:" vào các container cụ thể
    container_divs = soup.find_all('div', class_='container m-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4')
    for container in container_divs:
        description_tag = soup.new_tag('p')
        description_tag.string = 'Dưới đây là các nhóm:'
        container.insert(0, description_tag)

    # Loại bỏ thuộc tính draggable="true" từ tất cả các thẻ div
    draggable_divs = soup.find_all('div', draggable="true")
    for draggable_div in draggable_divs:
        del draggable_div['draggable']

    # Lưu HTML đã chỉnh sửa vào file
    with open(thumuccon, "w", encoding="utf-8") as html_file:
        html_file.write(soup.prettify())

# Crawl các câu hỏi có trong bài thi
def crawl_question_html(thumuccon):
    confirm_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div[2]/div/div/div[2]/div[2]/div[2]/button[2]')
    confirm_button.click()
    time.sleep(1)

    all_question_button = driver.find_elements(By.XPATH, '//*[@id="lesson_name"]/div[3]/div/div/div[2]/button')

    vonglap = len(all_question_button) / 5

    outer_html = ''

    for i in range(int(vonglap)):
        button_to_page_question = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div[3]/div/div[3]/div/div/div[2]/button[' + str(5*i+1) + ']')
        button_to_page_question.click()
        time.sleep(1)
        all_question_on_page = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div[3]/div/div[1]/div[1]/div/div/div')

        outer_html += all_question_on_page.get_attribute('outerHTML')

        if all_question_on_page.find_elements(By.CSS_SELECTOR, '.react-select__control'):
            div_class_control = all_question_on_page.find_elements(By.CSS_SELECTOR, '.react-select__control')

            for div_control in div_class_control:
                parent_element = div_control.find_element(By.XPATH, '..')
                parent_html = parent_element.get_attribute('outerHTML')
                driver.execute_script("arguments[0].scrollIntoView(true);", div_control)
                time.sleep(1)
                div_control.click()
                time.sleep(0.2)

                div_class_menu = driver.find_elements(By.CSS_SELECTOR, '.react-select__menu')[0]

                outer_html = outer_html.replace(parent_html, " (Chọn một trong các đáp án: " + div_class_menu.get_attribute('outerHTML') + ")")

                outer_html = outer_html.replace("Xóa lựa chọn", "Cột bên phải")

    outerHTMLtoSoup(outer_html, thumuccon)

def crawl(thumuclon):
    year = ' - 2024 - 2025'
    driver.get("https://thi.trangnguyen.edu.vn/thu-tai/")
    time.sleep(1)

    dethi_button = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[1]/div[1]/div/button')
    for i, dethi_div in enumerate(dethi_button):
        # if i != 0:
        #     continue

        print(i)
        driver.get("https://thi.trangnguyen.edu.vn/thu-tai/")
        time.sleep(1)
        dethi_div = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[1]/div[1]/div/button[' + str(i + 1) + ']')
        thumucbe = thumuclon + '/' + str(i + 1) + ' - ' + clean_folder_name(dethi_div.text)
        mkdir(thumucbe)
        dethi_div.click()

        time.sleep(1)

        vongthi_all_div = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/table/tbody/tr')

        print(range(len(vongthi_all_div)))
        for j in range(len(vongthi_all_div)):
            # print(j)
            # if j > 6:
            #     continue

            if j != 0:
                try:
                    driver.back()
                    time.sleep(0.5)
                    alert = Alert(driver)  
                    alert.accept() 
                except Exception as e:
                    print("Không có alert:", str(e))

            time.sleep(1)

            try:
                dethi = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[1]/div[1]/div/button[' + str(i + 1) + ']')
                dethi.click()
                time.sleep(1)

                vongthi_all_div = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/table/tbody/tr')
                driver.execute_script("arguments[0].scrollIntoView(true);", vongthi_all_div[j])
                time.sleep(1)
                thumuccon = thumucbe + '/' + str(j + 1) + ' - ' + clean_file_name(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/table/tbody/tr[' + str(j + 1) + ']/td[2]').text) + year + '.html'
                vongthi_all_div[j].click()
                time.sleep(1)

                crawl_question_html(thumuccon)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
        
        time.sleep(1)

    driver.quit()

def main_crawl_question(link_page, account, password, path_folder):
    print("Crawl câu hỏi")
    mkdir(path_folder)

    login(link_page, account, password)
    crawl(path_folder)

if __name__ == "__main__":
    link_page = 'https://trangnguyen.edu.vn/dang-nhap'
    account = 'account1'
    password = 'password1'
    path_folder = 'Khoi 1'
    main_crawl_question(link_page, account, password, path_folder)