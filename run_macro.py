#!/usr/bin/env python3
import pyautogui
import time

def do_macro():
    time.sleep(0.1)
    print("Copying (Ctrl+C)...")
    pyautogui.hotkey('ctrl', 'c')
    
    time.sleep(0.1)
    print("Copying (Ctrl+C)...")
    print("Switching window (Alt+Tab)...")
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    
    pyautogui.keyDown('backspace')
    time.sleep(1)
    pyautogui.keyUp('backspace')
    print("Pasting (Ctrl+V)...")
    pyautogui.hotkey('ctrl', 'v')
    print("Pressing Enter...")
    pyautogui.press('enter')

    print("Macro completed.")

if __name__ == "__main__":
    do_macro()
