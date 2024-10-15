import random
from fake_useragent import UserAgent
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException
)
from time import sleep

ua = UserAgent()
headers = {"user-agent": ua.random}
print(headers)

def captcha(driver):
    try:
        text_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Подтвердите, что запросы отправляли вы, а не робот')]")
        if text_element:
            button = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.ID, "js-button"))
                    )
            if button:
                button.click()
                print('вышла капча и была решена')
            else:
                print('не удалось решить капчу')
        else:
            print("captcha no")
    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
        print(f'Ошибка капчи: {e}')


# def transit(driver):
#     try:
#         transition = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "g1e24ca2b"))
#             # EC.element_to_be_clickable((By.CLASS_NAME, "/html/body/main/div/div[1]/a"))
#         )
#         print('задержка')
#         time.sleep(15)
#         if transition:
#             transition.click()
#             print('вышла хуйня с переходом и переход выполнен')
#         else:
#             print('переход невыполнен')
#     except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
#         print(f"ошибка с хуйней с переходом: {e}")

def wind(driver):
    try:
        wind_no = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME,"styles_root__EjoL7"))
        )
        if wind_no:
            wind_no.click()
            print('Элемент окно найден и кликнут')
            return True
        else:
            print('Элемент окно не найден')
    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
        # print(f"ошибка с окном не сейчас: {e}")
        return False
        

            # win = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME,"watch-online-button"))
            # )
def selen(site):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers['user-agent']}")
    driver = webdriver.Chrome(options=options)
    https://hd.kinopoisk.ru/film/0a189088712f48da8f23075548fa0a29
    https://hd.kinopoisk.ru/film/d9a6edaa99c64111b1df36dcced246ea?rt=0a189088712f48da8f23075548fa0a29
    https://hd.kinopoisk.ru/film/d9a6edaa99c64111b1df36dcced246ea?rt=db0b5657995f48e79ff6138c649dc068
    https://hd.kinopoisk.ru/film/d9a6edaa99c64111b1df36dcced246ea
    try:
        driver.maximize_window()
        driver.get(url=site)

        sleep(100)
        captcha(driver)
        
        try:
            sleep(7)
            win = driver.find_element(By.CLASS_NAME, 'watch-online-button')
            if win:
                win.click()
            else:
                try:
                    win2 = driver.find_element(By.NAME, 'Смотреть сериал')
                    if win2:
                        win2.click()
                except (NoSuchElementException, ElementNotInteractableException) as ex:
                    print(f"ошибка при поиске или клике по win2: {ex}")
        except (NoSuchElementException, ElementNotInteractableException) as ex:
            print(f"ошибка при поиске или клике по win: {ex}")
    except (TimeoutException, WebDriverException) as ex:
        print(f"ошибка при инициализации или загрузке страницы: {ex}")
    finally:
        driver.quit()
                # win2 = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.CLASS_NAME,"styles_button__1_G0A"))
                # )style_iconLeft__Kq1ig
                # win2 = driver.find_element(By.CLASS_NAME, 'style_iconLeft__Kq1ig')
                # win2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/div/main/div[1]/div/div/section/div/div[2]/section/div[2]/div/div[2]/div[1]/button')
                # style_button__PNtXT styles_button_watch__8ovJc style_buttonSize52__b5OBe style_buttonPlus__TjQez style_buttonLight____6ma style_withIconLeft___Myt9
            # try:
            #     wind_no = WebDriverWait(driver, 10).until(
            #         EC.element_to_be_clickable((By.CLASS_NAME,"styles_root__EjoL7"))
            #     )
            #     if wind_no:
            #         wind_no.click()
            #         print('Элемент окно найден и кликнут')
            #     else:
            #         print('Элемент окно не найден')

            # except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
            #     print(f"ошибка с окном не сейчас: {e}")

            # try:
            #     entrance = WebDriverWait(driver, randw).until(
            #         EC.element_to_be_clickable((By.CLASS_NAME, 'styles_loginButton__LWZQp'))
            #     )
            #     if entrance:
            #         entrance.click()
            #         print('Элемент ВХОД найден и кликнут')
            #     else:
            #         print('Элемент ВХОД не найден')

            # except (NoSuchElementException, TimeoutException) as e:
            #     print(f'ошибка ВХОД не найден или не кликабелен: {e}')
            # except ElementNotInteractableException:
            #     print(f"ошибка ВХОД не взаимодействуем: {e}")

            # print("задержка 1000")
            # time.sleep(1000)
    # except (Exception, TimeoutException) as ex:
    #     print(f"ошибка: {ex}")
    #         # driver.quit()
    #         # continue
    # finally:
    #     time.sleep(5)
    #     driver.quit()



selen('https://hd.kinopoisk.ru/')
# selen('https://www.kinopoisk.ru/')
        # try:
        #     button = WebDriverWait(driver, 7).until(
        #             EC.element_to_be_clickable((By.ID, "js-button"))
        #             )
        #     time.sleep(15)
        
        #     if button:
        #         button.click()
        #         print('вышла капча и была решена')
        #     else:
        #         print('не удалось решить капчу')
        
        # except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
        #     print(f'Ошибка капчи: {e}')

