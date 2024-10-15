import faker
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

def read_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

ua = UserAgent()

def get_fake_data(data_type, n):
    f = faker.Faker('ru_RU')
    if data_type == 'email':
        return [f.email() for _ in range(n)]
    
    elif data_type == 'first_name':
        return [f.first_name() for _ in range(n)]
    
    elif data_type == 'last_name':
        return [f.last_name() for _ in range(n)]
    
    elif data_type == 'name':
        return [f.name() for _ in range(n)]
    
    elif data_type == 'middle_name':
        return [f.middle_name() for _ in range(n)]
    else:
        raise ValueError("Неподдерживаемый тип данных")

# Основная функция для работы с Selenium
def selen(site, phone_number):
    options = uc.ChromeOptions()
    headers = {"user-agent": ua.random}
    options.add_argument(f"user-agent={headers['user-agent']}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = uc.Chrome(options=options)
    ema = get_fake_data('email', 1)[0]
    first_name = get_fake_data('first_name', 1)[0]
    last_name = get_fake_data('last_name', 1)[0]
    middle_name = get_fake_data('middle_name', 1)[0]

    try:
        # rnd = random.randrange(1, 10)
        driver.maximize_window()
        driver.get(url=site)
        sleep(2)
        lstnm = driver.find_element(By.ID, "LastName")
        lstnm.send_keys(last_name)
        lstnm.send_keys(Keys.ENTER)
        sleep(2)
        fstnm = driver.find_element(By.ID, "FirstName")
        fstnm.send_keys(first_name)
        sleep(2)
        mdnm = driver.find_element(By.ID, "MiddleName")
        mdnm.send_keys(middle_name)
        mdnm.send_keys(Keys.ENTER)
        sleep(2)
        phon = driver.find_element(By.ID, "Phone")
        phon.send_keys(phone_number)
        phon.send_keys(Keys.ENTER)
        sleep(2)
        mail = driver.find_element(By.ID, "Email")
        mail.send_keys(ema)
        mail.send_keys(Keys.ENTER)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "errorLabel"))
        )
        if button:
            return True
        sleep(2)
    except (TimeoutException, WebDriverException) as ex:
        # print(f"ошибка при инициализации или загрузке страницы: {ex}")
        return False
    finally:
        driver.close()
        driver.quit()

def write_registered_number(file_path, phone_number):
    with open(file_path, 'a') as file:
        file.write(phone_number + '\n')

phone_numbers = read_numbers_from_file('numb.txt')
for phone_number in phone_numbers:
    if selen("https://m.paylate.ru/Registration", phone_number):
        write_registered_number('registered_numbers.txt', phone_number)
        print(f"INFO: {phone_number} выписал")
    else:
        print(f"INFO: {phone_number} не зарегистрирован")

