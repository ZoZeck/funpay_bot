import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Script:
    def __init__(self, driver):
        self.driver = driver

    def funpay_auto_update(self):
        self.driver.get('https://funpay.com/lots/461/trade')
        time.sleep(2)
        button = self.driver.find_element('xpath',
                                          '//*[@id="content"]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/button').click()

    def funpay_auto_sell(self):
        items = ['Golden', 'Skull', 'Mask', 'for', 'The', 'Trickster']
        items_tuple = ('Golden Skull Mask for The Trickster')
        selling_item = []
        while True:
            self.driver.get('https://funpay.com/')
            sales_gonk = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul[2]/li[2]/a/span')
            time.sleep(2)
            # Если поступает продажа или продажа существует, запуск процесса
            if int(sales_gonk.text) >= 1:
                self.driver.get('https://funpay.com/orders/trade')
                new_sale = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[1]')
                sale_description = new_sale.find_element(By.XPATH, '//*[@class="order-desc"]/div[1]')
                # Нахождение названия предмета
                for i in sale_description.text.split():
                    if i in items:
                        selling_item.append(i)
                        item = ' '.join(selling_item)
                if bool(item in items_tuple) == True:
                    # Нахождение номера заказа
                    for i in new_sale.find_element(By.XPATH, '//*[@class="tc-order"]').text.split():
                        if i.startswith('#'):
                            sale_number = i
                    time.sleep(2)
                    # Проверка всех старых номеров заказов
                    with open(f'sales_num.txt', 'r') as txt:
                        sales_numbers = txt.read()
                        txt.close()
                    print(sale_number, ' <-- Номер последний продажи')
                    # Сравнение старых номеров с новым
                    if sale_number in sales_numbers:
                        print('\n-- Продажа уже была осуществлена --')
                    # Если номера в файле не оказывается, осуществляем продажу
                    else:
                        new_numbers = sale_number + ' ' + sales_numbers
                        # Записываем новый номер в БД
                        with open(f'sales_num.txt', 'r+') as txt:
                            txt.write(f'{str(new_numbers)}\n')
                            txt.close()
                            print('Номер продажи был записан')
                        # Нахождение первого кода, с последующим удалением и отправкой
                        with open(f'codes\\{item}.txt', 'r') as txt:
                            code_to_send = txt.readlines()[0]
                            print(code_to_send, ' <-- Sending this code')
                            txt.close()
                        # Сохранение всех кодов кроме первого
                        with open(f'codes\\{item}.txt', 'r') as txt:
                            code_to_save = txt.readlines()[1:]
                            txt.close()
                        # Удаление первого кода
                        with open(f'codes\\{item}.txt', 'w') as txt:
                            for i in code_to_save:
                                txt.write(i)
                                txt.close()
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
                                    Ключ — "{code_to_send}"\n
                                    После завершения проверки аккаунта:
                                    1️⃣ Пожалуйста, зайдите в раздел "Мои покупки", выберите соответствующий заказ и нажмите кнопку "Подтвердить выполнение заказа";
                                    2️⃣ Если Вам не сложно — оставьте отзыв о моей работе!'''
                        chat = self.driver.find_element(By.XPATH, '//*[@id="comments"]/textarea')
                        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, chat, text)
                        self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/form/div[3]/button').click()
            time.sleep(10)



def main():
    options = Options()
    options.add_argument('user-data-dir=C:\\Users\\coolm\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    driver = webdriver.Chrome(executable_path=r'chromedriver\\chromedriver.exe', chrome_options=options)

    while True:
        time.sleep(2)
        watcher = Script(driver)
        # watcher.funpay_auto_update()
        watcher.funpay_auto_sell()
        time.sleep(2)

if __name__ == "__main__":
    main()