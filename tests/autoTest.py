import time

import pyautogui

start_time = time.time()

# Open DIAD
pyautogui.moveTo(712, 183)
pyautogui.click()
time.sleep(3)

# Click start
pyautogui.moveTo(712, 234)
pyautogui.click()
time.sleep(3)

# Choose screenshot area
pyautogui.moveTo(712, 356)
pyautogui.mouseDown()
pyautogui.moveTo(712 + 200, 356 + 200)
pyautogui.mouseUp()
time.sleep(3)

# Click start detection
pyautogui.moveTo(812, 234)
pyautogui.click()

print('Test finished time cost:', time.time() - start_time)
