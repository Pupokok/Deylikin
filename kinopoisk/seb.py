# from seleniumbase import SB

# with SB(headed=True) as driver:
#     driver.open('https://www.kinopoisk.ru/')
#     # driver.cl

import faker

f = faker.Faker()

def get_list_of_email(n):
    return [f.email() for _ in range(n)]

# or just print
for i in range(10):
    print(f.email()) 