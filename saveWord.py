import re
import os
import time
import pyautogui
import pyperclip
from bs4 import BeautifulSoup

TIME_KEY = 0.2
TIME_LONG = 1

def keyRight():
    pyautogui.press('right')
    pyautogui.keyUp('right')
    time.sleep(TIME_KEY)

def keyLeft():
    pyautogui.press('left')
    pyautogui.keyUp('left')
    time.sleep(TIME_KEY)

def keyBackspace():
    pyautogui.press('backspace')
    pyautogui.keyUp('backspace')
    time.sleep(TIME_KEY)

def keyTab():
    pyautogui.press('tab')
    pyautogui.keyUp('tab')
    time.sleep(TIME_KEY)

def keyEnter():
    pyautogui.press('enter')
    pyautogui.keyUp('enter')
    time.sleep(TIME_KEY)

def editText(text):
    pyautogui.keyDown('shift')
    pyautogui.press(text)
    pyautogui.keyUp(text)
    pyautogui.keyUp('shift')
    time.sleep(TIME_KEY)

def openReplaceDialog():
    pyautogui.keyDown('ctrl')
    pyautogui.press('h')
    pyautogui.keyUp('h')
    pyautogui.keyUp('ctrl')
    time.sleep(TIME_LONG)


def edit_text_word(text):
    keyRight()
    keyLeft()
    # keyLeft()
    keyBackspace()
    editText(text)
    keyTab()
    keyRight()
    keyLeft()
    keyLeft()
    keyBackspace()
    editText(text)
    keyTab()
    keyTab()
    keyTab()
    keyEnter()
    keyEnter()

    if text == 'd':
        keyTab()
        keyTab()
        keyTab()
        keyTab()
        keyTab()
        keyTab()
        keyEnter()

def edit_word(duong_dan_tep_moi):
    os.startfile(duong_dan_tep_moi)
    time.sleep(3)

    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('v')
    pyautogui.keyUp('ctrl')
    time.sleep(2)

    openReplaceDialog()
    edit_text_word('a')
    edit_text_word('b')
    edit_text_word('c')
    edit_text_word('d')

    pyautogui.keyDown('ctrl')
    pyautogui.press('s')
    pyautogui.keyUp('s')
    pyautogui.keyUp('ctrl')
    time.sleep(2)

    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('f4')
    pyautogui.keyUp('alt')
    time.sleep(2)

def split_caption_img(string):
    parts = string.split("Image:")
    image_url = parts[1].strip()
    
    return image_url    

def convert_string_img_to_html(soup, text):
    url_pattern = r'Image:\s*(https?://[^\s)\]]+)'
    matches = re.finditer(url_pattern, text)

    p_tag = soup.new_tag("p")

    last_end = 0
    for match in matches:
        start, end = match.span()
        p_tag.append(text[last_end:start]) 
        img_tag = soup.new_tag("img", src=match.group(1))
        p_tag.append(img_tag)
        last_end = end

    p_tag.append(text[last_end:])
    return p_tag

# Đưa Txt về HTML để render ảnh
def txt_to_html(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    soup = BeautifulSoup("", "html.parser")

    line_xoaluachon = 0

    for line in lines:
        line = line.strip()

        if "Xóa lựa chọn" in line:
            line_xoaluachon = 1
            continue

        if line_xoaluachon:
            line_xoaluachon = 0
            continue

        if "Image:" in line:
            p_tag = convert_string_img_to_html(soup, line)
            soup.append(p_tag)

        elif line:
            p_tag = soup.new_tag("p")
            p_tag.string = line
            soup.append(p_tag)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    
    os.startfile(output_file)

    time.sleep(1)

    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    
    time.sleep(1)
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('c')
    pyautogui.keyUp('ctrl')

    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('w')
    pyautogui.keyUp('w')
    pyautogui.keyUp('ctrl')

def duyet_thu_muc(duong_dan):
    for thu_muc_goc, thu_muc_con, tap_tin in os.walk(duong_dan):
        if tap_tin:
            index = 0
            for ten_tap_tin in tap_tin:
                if 'answer.txt' in ten_tap_tin:
                    print(index)
                    duong_dan_tep_tin = os.path.join(thu_muc_goc, ten_tap_tin)

                    txt_to_html(duong_dan_tep_tin, duong_dan_tep_tin.replace('.txt', '.html'))


                    # with open(duong_dan_tep_tin, 'r', encoding='utf-8') as file:
                    #     noi_dung = file.read()

                    # pyperclip.copy(noi_dung)
                    # break

                    time.sleep(1)
                    duongdancu = duong_dan_tep_tin
                    duong_dan_tep_moi = duongdancu.replace('.txt', '.docx')

                    with open(duong_dan_tep_moi, 'w'):
                        pass
                    
                    time.sleep(1)

                    edit_word(duong_dan_tep_moi)

                    index += 1

def main_save_word(path_folder):
    print('Chuyển đổi TXT sang DOCX')
    duyet_thu_muc(path_folder)

if __name__ == "__main__":
    path_folder = 'Khoi 1'
    main_save_word(path_folder)