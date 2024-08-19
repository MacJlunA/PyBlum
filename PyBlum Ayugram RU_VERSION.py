# -*- coding: utf-8 -*-

import requests
import hashlib
import uuid
import base64
import json
import sys
import platform
import os
import time
import random
import pyautogui
import pygetwindow as gw
import keyboard
from pynput.mouse import Button, Controller
from colorama import Fore, Style, init

init(autoreset=True)

part1 = "github_pat_11ANT6DHA0zvlMrNZ3PZ7S_"
part2 = "TnsHse5LtW1xJ87peQEzWyJ3lx1KeCZ43aJrH3whBNIVOSD323Zh4q0sDnC"
GITHUB_TOKEN = part1 + part2
SCRIPT_URL = "https://raw.githubusercontent.com/MacJlunA/PyBlum/main/PyBlum%20Ayugram%20RU_VERSION.py"
GITHUB_REPO = 'MacJlunA/PyBlum'
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/contents'
VERSION_FILE_PATH = "script_version.txt"  # Путь к файлу с версией в репозитории
CURRENT_VERSION = "2.1.4"  # Ваша текущая версия
SCRIPT_FILE_NAME = os.path.basename(__file__)

# GitHub Token (если требуется)
GITHUB_TOKEN = part1 + part2

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
}

def get_script_version_from_github():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{VERSION_FILE_PATH}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        version = base64.b64decode(content['content']).decode('utf-8').strip()
        return version
    else:
        print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Не удалось получить версию скрипта с GitHub. Код ошибки: {response.status_code}")
        return None

def download_and_replace_script():
    response = requests.get(SCRIPT_URL)
    if response.status_code == 200:
        # Сохраняем новый скрипт с временным именем
        temp_file_path = "temp_script.py"
        with open(temp_file_path, 'wb') as file:
            file.write(response.content)
        
        # Заменяем текущий скрипт новым
        os.replace(temp_file_path, os.path.basename(__file__))
        print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Скрипт обновлен. Перезапустите его для применения изменений.")
        time.sleep(5)
        exit()
    else:
        print(f"[{Fore.RED}PyBlum{Style.RESET_ALL}] | Ошибка при загрузке обновления. Код ошибки: {response.status_code}")

def check_for_updates():
    latest_version = get_script_version_from_github()
    if latest_version is None:
        print(f"[{Fore.RED}PyBlum{Style.RESET_ALL}] | Проверка обновлений не удалась.")
        return
    
    if latest_version > CURRENT_VERSION:
        print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Доступна новая версия скрипта: {latest_version}")
        response = input(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Хотите загрузить обновление? (y/n): ").strip().lower()
        
        if response == 'y':
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Загрузка обновления...")
            download_and_replace_script()
        else:
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Обновление отменено.")
    else:
        print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | У вас установлена последняя версия скрипта: {CURRENT_VERSION}.")
        time.sleep(2)

def check_script_version():
    latest_version = get_script_version_from_github()
    if latest_version is not None:
        if latest_version == CURRENT_VERSION:
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Версия скрипта актуальна.")
            print("пенис")
        else:
            check_for_updates()
    else:
        print(f"[{Fore.RED}PyBlum{Style.RESET_ALL}] | Ошибка при проверке версии")
        time.sleep(3)
        exit()


# Call this function to check the script version
check_script_version()

# Function to get file content from GitHub
def get_file_content(file_path):
    response = requests.get(f'{GITHUB_API_URL}/{file_path}', headers=headers)
    if response.status_code == 200:
        content = response.json().get('content')
        if content:
            decoded_content = base64.b64decode(content).decode('utf-8')
            return decoded_content
    return None


# Function to update file content on GitHub
def update_file_content(file_path, content, sha):
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        'message': f'Update {file_path}',
        'content': encoded_content,
        'sha': sha
    }
    response = requests.put(f'{GITHUB_API_URL}/{file_path}', headers=headers, json=data)
    return response.status_code == 200


# Function to get file SHA from GitHub
def get_file_sha(file_path):
    response = requests.get(f'{GITHUB_API_URL}/{file_path}', headers=headers)
    if response.status_code == 200:
        return response.json().get('sha')
    return None


# Function to get HWID (hashed)
def get_hwid():
    hwid = uuid.getnode()
    hwid_hashed = hashlib.sha256(str(hwid).encode()).hexdigest()
    return hwid_hashed


# Function to check if the key and HWID match
def check_key_hwid(user_key, hwid, keys_hwid_content):
    keys_hwid = json.loads(keys_hwid_content)
    if user_key in keys_hwid["keys"]:
        if keys_hwid["keys"][user_key] == "" or keys_hwid["keys"][user_key] == hwid:
            return True
    return False


# Function to bind key to HWID
def bind_key_hwid(user_key, hwid, keys_hwid_content, file_path):
    keys_hwid = json.loads(keys_hwid_content)
    keys_hwid["keys"][user_key] = hwid
    new_content = json.dumps(keys_hwid, indent=4)
    sha = get_file_sha(file_path)
    update_file_content(file_path, new_content, sha)


# Function to authorize the user key
def authorize(user_key):
    hwid = get_hwid()
    keys_hwid_content = get_file_content('keys_hwid.json')
    if keys_hwid_content is not None:
        if check_key_hwid(user_key, hwid, keys_hwid_content):
            bind_key_hwid(user_key, hwid, keys_hwid_content, 'keys_hwid.json')
            return "Успех!"
            time.sleep(1)
        else:
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Введен неверный ключ.")
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Приобрести можно в Телеграм @ClickerForBlum")
            time.sleep(3)
            return "Ошибка авторизации!"
            time.sleep(5)
    else:
        print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Напишите в лс администратору со скриншотом данной ошибки. Telegram: @loserificc")
        time.sleep(3)
        return "Ошибка!"
        time.sleep(5)

def save_license_key(key):
    with open(KEY_FILE_PATH, 'w') as key_file:
        key_file.write(key)

KEY_FILE_PATH = "C:\\license_key.txt"

def load_license_key():
    if os.path.exists(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, 'r') as key_file:
            return key_file.read().strip()
    return None

# Function to prompt the user to enter a license key
def enter_license_key():
    key = load_license_key()
    
    if key:
        print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Авторизация автоматическая, ваш ключ {key}.")
        print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Ключ действителен до 01.01.2033")
        time.sleep(2)
        result = authorize(key)
        if result == "Успех!":
            time.sleep(1)
            clear_console()
            return
        else:
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Неверный ключ.")
    
    try:
        key = input(f'[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Введите ключ: ')
        result = authorize(key)
        if result == "Успех!":
            save_license_key(key)
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Успешная авторизация.")
            time.sleep(1)
            clear_console()
        else:
            print(result)
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)


# Initialize colorama for colored terminal output
init(autoreset=True)


# Function to clear the console
def clear_console():
    if platform.system() == 'Windows':
        os.system('cls & title Python Example')
    elif platform.system() in ['Linux', 'Darwin']:
        os.system('clear')
        sys.stdout.write("\x1b]0;Python Example\x07")

if sys.version_info.minor < 10:
    print("Error: Python version must be 3.10 или выше")
    sys.exit(1)

enter_license_key()

mouse = Controller()

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

def check_window(name):
    return gw.getWindowsWithTitle(name)

def select_delay():
    print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Выберите скорость кликов..")
    print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | 1. 0.001 секунда")
    print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | 2. 0.010 секунд")
    choice = input(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Enter 1, 2: ")
    if choice == '1':
        return 0.001
    elif choice == '2':
        return 0.010
    else:
        print(f"{Fore.RED}[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Ошибка, используется 0.001")
        return 0.001

delay = select_delay()

def find_window():
    window_name = "AyuGramDesktop"
    check = check_window(window_name)
    while not check:
        clear_console()
        window_name = input(
            f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Blum {Fore.RED}не найден!{Style.RESET_ALL} Нажмите Enter что бы попробовать снова:")
        if window_name == '':
            check = check_window("AyuGramDesktop")
        else:
            check = check_window(window_name)

    if not check:
        print(
            f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Blum {Fore.RED}не найден!{Style.RESET_ALL} Exiting program.")
        time.sleep(1.5)
        sys.exit(1)

    clear_console()
    print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Blum {Fore.GREEN}найден.{Style.RESET_ALL}")
    return check[0]

telegram_window = find_window()

print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Button {Fore.GREEN}'E'{Style.RESET_ALL} запускает программу.")
print(
    f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Button {Fore.GREEN}'ESC'{Style.RESET_ALL} выходит из программы.")
print(
    f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | Button {Fore.GREEN}'R'{Style.RESET_ALL} ставит программу на паузу.")

paused = False

while not keyboard.is_pressed('e'):
    time.sleep(0.1)

print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | {Fore.GREEN}Запуск...{Style.RESET_ALL}")

def is_safe_to_click(r, g, b):
    return (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255))

def perform_custom_action():
    window_title = "AyuGramDesktop"
    all_windows = gw.getWindowsWithTitle(window_title)

    if all_windows:
        window = all_windows[0]
        window.activate()
        time.sleep(0.5)

        window_left = window.left
        window_top = window.top
        window_width = window.width
        window_height = window.height

        center_x = window_left + window_width // 2
        center_y = window_top + window_height // 2

        new_y = center_y - -230

        pyautogui.moveTo(center_x, new_y)
        pyautogui.click()

def main_loop():
    global paused
    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    while True:
        if keyboard.is_pressed('esc'):
            print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | {Fore.RED}Выходим...{Style.RESET_ALL}")
            time.sleep(2)
            break

        if keyboard.is_pressed('r'):
            paused = not paused
            if paused:
                print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | {Fore.YELLOW}Пауза...{Style.RESET_ALL}")
            else:
                print(f"[{Fore.LIGHTMAGENTA_EX}PyBlum{Style.RESET_ALL}] | {Fore.GREEN}Продолжаем...{Style.RESET_ALL}")
            time.sleep(0.2)

        if paused:
            continue

        if telegram_window:
            try:
                telegram_window.activate()
            except:
                telegram_window.minimize()
                telegram_window.restore()

        screenshot = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))
        width, height = screenshot.size

        for x in range(0, width, 20):
            for y in range(0, height, 20):

                r, g, b = screenshot.getpixel((x, y))
                if is_safe_to_click(r, g, b):
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x, screen_y)
                    time.sleep(delay)
                    break

        if delay == 0.5:
            perform_custom_action()
            time.sleep(delay)

main_loop()

time.sleep(2)
sys.exit(0)
