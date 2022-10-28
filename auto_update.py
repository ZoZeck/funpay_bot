import time

from threading import Timer
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def update(driver):
    while True:
        driver.get('https://funpay.com/lots/461/trade')
        rise_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/button')
        # Dead By Daylight
        if rise_button.text == 'Поднять предложения':
            rise_button.click()
        time.sleep(2)
        print(f'\nDead By Daylight\n',
              driver.find_element(By.XPATH, '//*[@id="site-message"]').text,
              f'\nСейчас: {datetime.now().hour}ч:{datetime.now().minute}м')
        # Пополнение баланса
        driver.get('https://funpay.com/lots/1086/trade')
        rise_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/button')
        if rise_button.text == 'Поднять предложения':
            rise_button.click()
        time.sleep(2)
        print(f'\nПополнение баланса\n',
              driver.find_element(By.XPATH, '//*[@id="site-message"]').text,
              f'\nСейчас: {datetime.now().hour}ч:{datetime.now().minute}м')
        # Ключи Steam
        driver.get('https://funpay.com/lots/1008/trade')
        rise_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/button')
        if rise_button.text == 'Поднять предложения':
            rise_button.click()
        time.sleep(2)
        print(f'\nКлючи Steam\n',
              driver.find_element(By.XPATH, '//*[@id="site-message"]').text,
              f'\nСейчас: {datetime.now().hour}ч:{datetime.now().minute}м')
        time.sleep(1800)


def main():
    options = Options()
    # options.add_argument('user-data-dir=C:\\Users\\coolm\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    options.add_argument('user-data-dir=C:\\Users\\coolm\\AppData\\Local\\Google\\Chrome\\User Data\\Guest Profile')
    options.add_argument('--window-size=1280,720')
    options.add_argument('--headless')
    options.add_argument("--mute-audio")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(executable_path=r'chromedriver\\chromedriver.exe', chrome_options=options)

    update(driver)




if __name__ == "__main__":
    main()