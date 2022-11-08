import os
import time

from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from telegram_bot import send_message


def nums_editor(method, order_number):
    method, order_number = method, order_number
    if method == 'read':
        with open(f'{os.getcwd()}\\Data\\sales_nums.txt', 'r') as sales_nums_txt:
            sales_nums = sales_nums_txt.read().split()
            sales_nums_txt.close()
        return sales_nums
    elif method == 'write':
        with open(f'{os.getcwd()}\\Data\\sales_nums.txt', 'r+') as sales_nums_txt:
            sales_nums_txt.write(str(order_number))
            sales_nums_txt.close()


def code_editor(selling_item, amount):
    selling_item, amount = selling_item, amount
    with open(f'{os.getcwd()}\\Data\\Codes\\{selling_item}.txt', 'r+') as codes_txt:
        code_to_send = codes_txt.readlines()[:amount]
        codes_txt.close()
    with open(f'{os.getcwd()}\\Data\\Codes\\{selling_item}.txt', 'r+') as codes_txt:
        code_to_save = codes_txt.readlines()[amount:]
        codes_txt.close()
    with open(f'{os.getcwd()}\\Data\\Codes\\{selling_item}.txt', 'r+') as codes_txt:
        for i in code_to_save:
            codes_txt.write(i)
        codes_txt.close()
    return code_to_send


def code_text(code_to_send):
    your_code = []
    for i in code_to_send:
        your_code.append(f'Ключ — "{i[:-1]}"\n')
    return your_code


class AutoSale:
    def __init__(self, driver):
        self.driver = driver
        self.categories = ['Dead by Daylight, Прочее', 'Twitch, Аккаунты', 'Steam, Пополнение баланса']
        self.selling_items = []
        self.items = ['Golden', 'Skull', 'Mask', 'for', 'The', 'Trickster',
                      'Амулет', 'Перья', 'Гордости',
                      'New', 'Vegas', 'Ultimate', 'Edition']
        self.new_sale_check()

    def new_sale_check(self):
        while True:
            self.driver.implicitly_wait(5)
            self.driver.get('https://funpay.com/')
            time.sleep(10)
            sales_gonk = self.driver.find_element(By.XPATH, "//span[starts-with(@class, 'badge badge-trade')]")
            if sales_gonk.text == '':
                return
            elif int(sales_gonk.text) >= 1:
                self.new_sale_description()

    def new_sale_description(self):
        self.driver.implicitly_wait(5)
        self.driver.get('https://funpay.com/orders/trade')
        last_sale = self.driver.find_element(By.XPATH, "//*[starts-with(@class, 'tc-item')]")
        order_number = last_sale.find_element(By.XPATH, "//*[starts-with(@class, 'tc-order')]").text
        if order_number in nums_editor('read', ''):
            print(f'Продажа с номером {order_number}, уже была осуществлена')
            self.new_sale_check()
        elif order_number not in nums_editor('read', ''):
            nums_editor('write', order_number)
            print(f'Поступила новая продажа, с номером {order_number}')
            sale_category = last_sale.find_element(By.XPATH, "//*[starts-with(@class, 'text-muted')]").text
            sale_description = last_sale.find_element(By.XPATH, "//*[starts-with(@class, 'order-desc')]").text
            if sale_category not in self.categories:
                self.new_sale_check()
            elif sale_category in sale_category and sale_category == 'Twitch, Аккаунты':
                amount = 1
            elif sale_category in sale_category and sale_category == 'Steam, Пополнение баланса':
                send_message(order_number)
            else:
                for i in sale_description.split():
                    try:
                        amount = int(i)
                    except ValueError:
                        continue
                for item in sale_description.split():
                    if item in self.items:
                        self.selling_items.append(item)
                        selling_item = ' '.join(self.selling_items)
                self.send_code(code_text(code_editor(selling_item, amount)))

    def send_code(self, ready_code_text):
        ready_code_text = ready_code_text
        last_sale = self.driver.find_element(By.XPATH, "//*[starts-with(@class, 'tc-item')]").click()
        js_add_text_to_input = """
                      var elm = arguments[0], txt = arguments[1];
                      elm.value += txt;
                      elm.dispatchEvent(new Event('change'));
                      """
        text = f'''🟪🟪Благодарю за покупку🟪🟪\n
                {" ".join(ready_code_text)}\n
                После завершения проверки аккаунта:
                1️⃣ Пожалуйста, зайдите в раздел "Мои покупки", выберите
                соответствующий заказ и нажмите кнопку "Подтвердить выполнение заказа";
                2️⃣ Если Вам не сложно — оставьте отзыв о моей работе!'''
        chat = self.driver.find_element(By.XPATH, '//*[@id="comments"]/textarea')
        self.driver.execute_script(js_add_text_to_input, chat, text)
        send_button = self.driver.find_element(By.XPATH, "//button[starts-with(@class, 'btn btn-gray btn-round')]")
        send_button.click()
        time.sleep(2)


def main():
    options = Options()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(f'user-data-dir={os.getcwd()}\\FunPay_User')
    options.add_argument('--profile-directory=FunPay_Bot')

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('user-agent=Funpay_Bot')
    options.add_argument('--window-size=1440,900')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_argument('--headless') Почему-то не работает нормально
    options.add_argument("--mute-audio")
    service_object = Service(binary_path)

    driver = webdriver.Chrome(service=service_object, chrome_options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
              const newProto = navigator.__proto__
              delete newProto.webdriver
              navigator.__proto__ = newProto
              """
    })

    AutoSale(driver)


if __name__ == "__main__":
    main()
