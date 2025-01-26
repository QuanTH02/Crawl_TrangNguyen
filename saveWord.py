import os
import time
import pyautogui
import pyperclip

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
    keyLeft()
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

def duyet_thu_muc(duong_dan):
    for thu_muc_goc, thu_muc_con, tap_tin in os.walk(duong_dan):
        if tap_tin:
            index = 0
            for ten_tap_tin in tap_tin:
                if 'answer.txt' in ten_tap_tin:
                    print(index)
                    duong_dan_tep_tin = os.path.join(thu_muc_goc, ten_tap_tin)

                    with open(duong_dan_tep_tin, 'r', encoding='utf-8') as file:
                        noi_dung = file.read()

                    pyperclip.copy(noi_dung)

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
