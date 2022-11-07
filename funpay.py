import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class Script:
    def __init__(self, driver):
        self.driver = driver

    def funpay_auto_sell(self):
        items = ['Golden', 'Skull', 'Mask', 'for', 'The', 'Trickster',
                 '300к', 'BP', '&', '1к', 'радужных', 'осколков',
                 '400', '000', 'BloodPoints',
                 'Амулет', 'сковородка', 'из', 'PUBG', '(Frying', 'pan)',
                 'Амулет', 'Перья', 'Гордости',
                 'New', 'Vegas', 'Ultimate', 'Edition']

        items_tuple = ('Golden Skull Mask for The Trickster',
                       '300к BP & 1к радужных осколков',
                       '400 000 BloodPoints',
                       'Амулет сковородка из PUBG (Frying pan)',
                       'Амулет Перья Гордости',
                       'New Vegas Ultimate Edition')

        category_list = ['Dead by Daylight, Прочее',
                         'Twitch, Аккаунты',
                         'Fallout 76, Ключи']

        def check():
            while True:
                try:
                    time.sleep(5)
                    global selling_item
                    selling_item = []
                    self.driver.get('https://funpay.com/')
                    sales_gonk = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul[2]/li[2]/a/span')
                    time.sleep(5)
                    # Если поступает продажа или продажа существует, запуск процесса
                    if sales_gonk.text == '':
                        return
                    elif int(sales_gonk.text) >= 1:
                        new_sale_description()
                except NoSuchElementException:
                    try:
                        if self.driver.find_element(By.XPATH, "//*[starts-with(text(),'Connection timed out')]"):
                            time.sleep(10)
                        elif self.driver.find_element(By.XPATH, "//*[starts-with(text(),'502 Bad Gateway')]"):
                            time.sleep(10)
                    finally:
                        return


        def new_sale_description():
            self.driver.get('https://funpay.com/orders/trade')
            new_sale = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[1]')
            sale_description = new_sale.find_element(By.XPATH, '//*[@class="order-desc"]/div[1]')
            category = new_sale.find_element(By.CLASS_NAME, 'text-muted')
            time.sleep(2)
            # Проверка категории
            if category.text not in category_list:
                # print(sale_number, ' <-- Номер последний продажи')
                with open(f'sales_num.txt', 'r') as txt:
                    sales_numbers = txt.read()
                    txt.close()
                print(sales_numbers.split()[0], ' <-- Номер последний продажи')
                return
            else:
                # Кол-во предметов
                for i in sale_description.text.splitlines():
                    if category.text == 'Twitch, Аккаунты':
                        amount = 1
                    else:
                        amount = int(i.split()[-2])
                # Нахождение названия предмета
                for i in sale_description.text.split():
                    if i in items:
                        selling_item.append(i)
                        item = ' '.join(selling_item)
                        if item in items_tuple:
                            find_sell_number(new_sale, item, amount)

        def find_sell_number(new_sale, item, amount):
            # Нахождение номера заказа
            for i in new_sale.find_element(By.XPATH, '//*[@class="tc-order"]').text.split():
                if i.startswith('#'):
                    sale_number = i
            # Проверка всех старых номеров заказов
            with open(f'sales_num.txt', 'r') as txt:
                sales_numbers = txt.read()
                txt.close()
            print(sale_number, ' <-- Номер последний продажи')
            # Сравнение старых номеров с новым
            if sale_number in sales_numbers:
                print('-- Продажа уже была осуществлена --\n')
            # Если номера в файле не оказывается, осуществляем продажу
            else:
                new_numbers = sale_number + ' ' + sales_numbers
                # Записываем новый номер в БД
                with open(f'sales_num.txt', 'r+') as txt:
                    txt.write(f'{str(new_numbers)}\n')
                    txt.close()
                    print('Номер продажи был записан')
                find_code(new_sale, item, amount)

        def find_code(new_sale,item, amount):
            # Нахождение первого кода, с последующим удалением и отправкой
            with open(f'codes\\{item}.txt', 'r') as txt:
                code_to_send = txt.readlines()[:amount]
                print(code_to_send, ' <-- Sending this code')
                txt.close()
            # Сохранение всех кодов кроме первого
            with open(f'codes\\{item}.txt', 'r') as txt:
                code_to_save = txt.readlines()[amount:]
                txt.close()
            # Удаление первого кода
            with open(f'codes\\{item}.txt', 'w') as txt:
                for i in code_to_save:
                    txt.write(i)
                txt.close()
            send_code(new_sale, code_to_send)

        def code_text(code_to_send):
            youre_code = []
            for i in code_to_send:
                youre_code.append(f'Ключ — "{i[:-1]}"\n')
            return youre_code

        def send_code(new_sale, code_to_send):
            # Открытие чата с покупателем и отправка сообщения с кодом в чат
            time.sleep(2)
            new_sale.click()
            time.sleep(2)
            JS_ADD_TEXT_TO_INPUT = """
                          var elm = arguments[0], txt = arguments[1];
                          elm.value += txt;
                          elm.dispatchEvent(new Event('change'));
                          """
            text = f'''🟪🟪Благодарю за покупку🟪🟪\n
                        {" ".join(code_text(code_to_send))}\n
                        После завершения проверки аккаунта:
                        1️⃣ Пожалуйста, зайдите в раздел "Мои покупки", выберите соответствующий заказ и нажмите кнопку "Подтвердить выполнение заказа";
                        2️⃣ Если Вам не сложно — оставьте отзыв о моей работе!'''
            chat = self.driver.find_element(By.XPATH, '//*[@id="comments"]/textarea')
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, chat, text)
            time.sleep(2)
            send_button = self.driver.find_element(By.XPATH,
                                    '//*[@id="content"]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/form/div[3]/button').click()
            time.sleep(3)

        check()


def main():
    options = Options()
    # options.add_argument('user-data-dir=C:\\Users\\coolm\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    options.add_argument('user-data-dir=C:\\Users\\coolm\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('user-agent=coolm4432')
    '''Задаю размер окна, что бы при запуске с параметром --headless
                                                             все окошки зависящие от размера, были развернуты'''
    options.add_argument('--window-size=1280,720')
    # options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome(executable_path=r'chromedriver\\chromedriver.exe', chrome_options=options)
    # По идеи должен отключать видимость того, что используется Selenium
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
              const newProto = navigator.__proto__
              delete newProto.webdriver
              navigator.__proto__ = newProto
              """
    })


    while True:
        time.sleep(2)
        watcher = Script(driver)
        watcher.funpay_auto_sell()
        time.sleep(2)

if __name__ == "__main__":
    main()