import random
import logging

from time import sleep
from fake_useragent import UserAgent
from aiogram.fsm.context import FSMContext

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


logging.basicConfig(level=logging.INFO)


def uas():
    ua = UserAgent()
    while True:
        user_agent = ua.random
        if "Safari" not in user_agent and "Mobile" not in user_agent:
            break

    headers = {"user-agent": user_agent}
    print(headers)
    return headers


def captcha(driver):
    try:
        text_element = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha")
        if text_element:
            button = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.ID, "js-button"))
                    )
            if button:
                try:
                    button.click()
                    return True
                except ElementNotInteractableException:
                    logging.error('Проход капчи/провал')
                    return False  # Если кнопка не кликабельна

        logging.info('Капча не найдена/успех')
        return True
        
    except NoSuchElementException:
        logging.info('Капча не найдена/успех')
        return True
    except TimeoutException:
        logging.error('Не удалось найти кнопку капчи в отведенное время/провал')
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
            logging.info('Окно закрыто/успех')
            return True
        
    except (NoSuchElementException) as e:
        return True
    except (TimeoutException) as e:
        logging.error(f'Ошибка окна промо: {e}')
        return False


def ran():
    delay = random.randint(1, 10)
    sleep(delay)




async def selena(url, state: FSMContext):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={uas()['user-agent']}")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.maximize_window()
        driver.get(url=url)
        logging.info('Сайт загружен')
        sleep(7)

        cpt = captcha(driver)
        if cpt:
            logging.info('вышла капча и была решена')
        else:
            logging.info('капча не была решена')
            return
        sleep(8)
        
        wndpr = window_promo(driver)
        if wndpr:
            logging.info('вышло окно промо')
        else:
            logging.info('не вышло окно промо')

        win = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'watch-online-button')))
        if win:
            logging.info('BUTTON Смотреть онлайн VIEW')
            win.click()
        
        await state.update_data(driver=driver)


    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"ошибка: {e}")
    finally:
        pass


#Вход по телефону
async def log_in_phone(driver, phone):
    try:     
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-type="phone"]'))).click()
            ran()
            id_phone = driver.find_element(By.ID, 'passp-field-phone')
            id_phone.click()
            id_phone.clear()
            ran()
            id_phone.send_keys(phone + Keys.ENTER)
            logging.info('Попытка входа с помощью номера телефона.')
            return True

    except (NoSuchElementException, ElementNotInteractableException) as e:
        logging.error(f'Ошибка входа: {e}')
        return False
    

async def login_code_phone(driver, code_phone, passw):
    try:
        onecode = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'passp-field-phoneCode')))
        ran()
        onecode.send_keys(code_phone)
        ran()
        account = driver.find_element(By.CLASS_NAME, 'AccountsListItem-account')
        account.click()

        password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'passp-field-passwd')))
        password.send_keys(passw + Keys.ENTER)
        logging.info('Попытка входа с помощью номера телефона.')
        see_films = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'watch-online-button')))
        see_films.click()
    
    except (NoSuchElementException, ElementNotInteractableException) as e:
        logging.error(f'Ошибка входа: {e}')
        return False
    

#Вход по майл
async def log_in_mail(driver, mail_cl, passw):
    try:
        driver.find_element(By.CSS_SELECTOR, '[data-type="login"]').click()
        ran()
        mail = driver.find_element(By.NAME, 'login')
        mail.send_keys(mail_cl + Keys.ENTER)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-live='polite']"))
        )
        return False
    except TimeoutException:
        logging.info('Логин успешно принят. Переходим к вводу пароля.')
        password = driver.find_element(By.ID, 'passp-field-passwd')
        password.send_keys(passw + Keys.ENTER)
        return True
        
async def login_code_mail(driver, code_phone_mail):
    try:
        onecode = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'passp-field-phoneCode')))
        onecode.send_keys(code_phone_mail + Keys.ENTER)
        see_films = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'watch-online-button')))
        ran()
        see_films.click()
        logging.info('Попытка входа с помощью номера mail.')


    except (NoSuchElementException, ElementNotInteractableException) as e:
        logging.error(f'Ошибка входа: {e}')
        return False