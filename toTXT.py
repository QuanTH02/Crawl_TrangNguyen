import os
import time
import pyautogui

def duyet_thu_muc(duong_dan):
    for thu_muc_goc, thu_muc_con, tap_tin in os.walk(duong_dan):
        # print(thu_muc_goc)
        if tap_tin:
            for ten_tap_tin in tap_tin:
                duong_dan_tep_tin = os.path.join(thu_muc_goc, ten_tap_tin)

                time.sleep(1)
                os.startfile(duong_dan_tep_tin)

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

                time.sleep(1)
                duongdancu = duong_dan_tep_tin
                duong_dan_tep_moi = duongdancu.replace('.html', '.txt')

                with open(duong_dan_tep_moi, 'w'):
                    pass
                
                time.sleep(1)

                os.startfile(duong_dan_tep_moi)
                time.sleep(2)

                pyautogui.keyDown('ctrl')
                pyautogui.press('v')
                pyautogui.keyUp('v')
                pyautogui.keyUp('ctrl')
                time.sleep(2)

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

def main_to_TXT(path_folder):
    print('Chuyển đổi HTML sang TXT')
    duyet_thu_muc(path_folder)

if __name__ == "__main__":
    path_folder = 'Khoi 1'
    main_to_TXT(path_folder)