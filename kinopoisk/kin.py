import random
import logging

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from time import sleep
# from selenium.webdriver.common.action_chains import ActionChains
# import undetected_chromedriver as uc


ua = UserAgent()
while True:
    user_agent = ua.random
    if "Safari" not in user_agent and "Mobile" not in user_agent:
        break

headers = {"user-agent": user_agent}

print(headers)
logging.basicConfig(level=logging.INFO)


def captcha(driver):
    try:
        text_element = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha")
        if text_element:
            button = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.ID, "js-button"))
                    )
            if button:
                try:
                    logging.info('Капча найдена')
                    button.click()
                    return True
                except ElementNotInteractableException:
                    logging.error('Кнопка капчи не доступна для клика.')
                    return False  # Если кнопка не кликабельна

        logging.info('Капча не найдена')
        return True
        
    except NoSuchElementException:
        logging.error('Капча не найдена.')
        return True
    except TimeoutException:
        logging.error('Не удалось найти кнопку капчи в отведенное время.')
        return False
    except Exception as e:
        logging.error(f'Произошла ошибка при обработке капчи: {e}')
        return False

def window_promo(driver):
    try:
        wind = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "styles_container__Vswe4")) #Проверяет, присутствует ли элемент в DOM-дереве страницы, независимо от того, видим он или нет.
        )
        ran()
        if wind:
            cross = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "styles_root__EjoL7"))
        )
            cross.click()
            logging.info('Окно промо закрыто')
            return True
        
    except (NoSuchElementException) as e:
        return True
    except (TimeoutException) as e:
        logging.error(f'Ошибка окна промо: {e}')
        return False


def ran():
    delay = random.randint(1, 10)
    sleep(delay)


def log_in_mail(driver): 
    try:
        win = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'watch-online-button')))
        if win:
            logging.info('BUTTON Смотреть онлайн VIEW')
            win.click()

            # 1 - вход по email, 2 - вход по телефону
            mail_lohin = int(input("Введите '1' для входа по email, '2' для входа по телефону: "))
            attempts = 0
            max_attempts = 3
            
            while attempts < max_attempts:
                logging.info(f'Попытка входа в аккаунт {attempts + 1}')

                if mail_lohin == 1:
                    driver.find_element(By.CSS_SELECTOR, '[data-type="login"]').click()
                    ran()
                    mail = driver.find_element(By.NAME, 'login')
                    mail.click()

                    current_value = mail.get_attribute('value')
                    for _ in range(len(current_value)):
                        sleep(1)
                        mail.send_keys(Keys.BACKSPACE)

                    mail.send_keys(input('Введите LOGIN: ') + Keys.ENTER)

                    try:
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-live='polite']"))
                        )
                        # actions = ActionChains(driver)
                        # actions.double_click(element).perform()
                        logging.info('Неверный логин или пароль, попробуйте снова.')
                        attempts += 1

                    except TimeoutException:
                        logging.info('Логин успешно принят. Переходим к вводу пароля.')

                        password = driver.find_element(By.ID, 'passp-field-passwd')
                        password.send_keys(input('Введите пароль: '))
                        password.send_keys(Keys.ENTER)
                        onecode = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'passp-field-phoneCode')))
                        onecode.send_keys(input('Введите код: ') + Keys.ENTER)
                        see_films = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'watch-online-button')))
                        ran()
                        see_films.click()
                        return True

                elif mail_lohin == 2:
                    
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-type="phone"]'))).click()
                    ran()
                    id_phone = driver.find_element(By.ID, 'passp-field-phone')
                    id_phone.click()
                    id_phone.clear()
                    ran()
                    id_phone.send_keys(input('Введите номер телефона: ') + Keys.ENTER)


                    onecode = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'passp-field-phoneCode')))
                    ran()
                    onecode.send_keys(input('Введите код: '))
                    ran()
                    accounts = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label]')
                    for acc in accounts:
                        aria_label = acc.get_attribute('aria-label')
                        print(aria_label)
                    see_films = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'watch-online-button')))
                    ran()
                    see_films.click()
                    logging.info('Попытка входа с помощью номера телефона.')
                    return True

            logging.info('Превышено максимальное количество попыток входа.')
            return False

    except (NoSuchElementException, ElementNotInteractableException) as e:
        logging.error(f'Ошибка входа: {e}')
        return False



def selen(site):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers['user-agent']}")
    driver = webdriver.Chrome(options=options)
    try:
        driver.maximize_window()
        driver.get(url=site)
        logging.info('Сайт загружен')
        sleep(7)

        cpt = captcha(driver)
        if cpt:
            logging.info('вышла капча и была решена')
        else:
            logging.info('капча не была решена')
            return
        sleep(15)

        
        wndpr = window_promo(driver)
        if wndpr:
            logging.info('вышло окно промо')
        else:
            logging.info('не вышло окно промо')
            
        lgml = log_in_mail(driver)
        if lgml:
            logging.info('вход успешен')
        else:
            logging.info('вход не успешен')


    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"ошибка: {e}")
    finally:
        driver.quit()


selen('https://www.kinopoisk.ru/film/1037479/')