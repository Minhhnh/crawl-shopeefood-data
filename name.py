import os
import time
import copy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re

EXPORT_FILE_NAME = 'test.xlsx'


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=chrome_options, executable_path='./chromedriver.exe')


driver = setup_driver()
url = r"https://shopeefood.vn/da-nang"
driver.get(url)
time.sleep(3)


def find_category(driver):
    element = driver.find_elements(by=By.CLASS_NAME, value='category-item')
    if element:
        return element
    else:
        return False


def find_pages(driver):
    element = driver.find_elements(by=By.TAG_NAME, value='li')
    menu_items = driver.find_elements(by=By.CLASS_NAME, value='menu-item')
    pages = [page for page in element if page not in menu_items]
    if pages:
        return pages[1:-1]
    else:
        return False


def find_dishes(driver):
    element = driver.find_elements(
        by=By.CLASS_NAME, value='item-restaurant-row')
    if element:
        return element
    else:
        return False


def find_sellers(driver):
    element = driver.find_elements(
        by=By.CLASS_NAME, value='item-restaurant')
    if element:
        return element
    else:
        return False


category_id = 1
seller_id = 1
dish_id = 1
wait = WebDriverWait(driver, 10)

category_files = open('category.csv', 'w', newline='', encoding="utf-8")
seller_files = open('seller.csv', 'w', newline='', encoding="utf-8")
dish_files = open('dish.csv', 'w', newline='', encoding="utf-8")

category_headers = ['NameCategory']
seller_headers = ['UserId', 'NameUser', 'Address', 'Avatar']
dish_headers = ['FoodId', 'UserId', 'CategoryId',
                'NameFood', 'PriceFood', 'ImageFood']

category_writer = csv.DictWriter(category_files, delimiter=',',
                                 lineterminator='\n', fieldnames=category_headers)
category_writer.writeheader()
seller_writer = csv.DictWriter(seller_files, delimiter=',',
                               lineterminator='\n', fieldnames=seller_headers)
seller_writer.writeheader()
dish_writer = csv.DictWriter(dish_files, delimiter=',',
                             lineterminator='\n', fieldnames=dish_headers)
dish_writer.writeheader()

categories = wait.until(find_category)
while category_id < len(categories):
    category = categories[category_id]
    category_writer.writerow(
        {category_headers[0]: category.text})
    print(category.text)
    category.click()
    time.sleep(3)
    page_index = 0
    pages = wait.until(find_pages)
    while page_index < min(4,len(pages)):
        try:
            page = pages[page_index]
            print('page ',page.text)
            page.find_element_by_tag_name('a').click()
            # wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'a'))).click()
            time.sleep(2)
            driver.execute_script(
                "window.scrollTo({ left: 0, top: document.body.scrollHeight/2, behavior: 'smooth'});")
            time.sleep(2)
            seller_index = 0
            sellers = wait.until(find_sellers)
            while seller_index < len(sellers):
                seller = sellers[seller_index]

                name_user = seller.find_element(
                    by=By.CLASS_NAME, value='name-res').text.strip()
                address = seller.find_element(
                    by=By.CLASS_NAME, value='address-res').text.strip()
                avatar = seller.find_element_by_tag_name(
                    'img').get_attribute("src")

                seller_writer.writerow(
                    {seller_headers[0]: seller_id, seller_headers[1]: name_user, seller_headers[2]: address, seller_headers[3]: avatar})

                print("Quán: ", name_user)
                # print(address)
                # print(avatar)

                seller_inside = seller.find_element(by=By.TAG_NAME, value='a')
                driver.execute_script(
                    "arguments[0].removeAttribute('target')", seller_inside)
                seller.click()
                time.sleep(3)
                driver.execute_script(
                    "window.scrollTo({ left: 0, top: document.body.scrollHeight/2, behavior: 'smooth'});")
                time.sleep(1)
                driver.execute_script(
                    "window.scrollTo({ left: 0, top: document.body.scrollHeight/2, behavior: 'smooth'});")
                time.sleep(1)
                dishes = wait.until(find_dishes)
                for dish in dishes:
                    dish_name = dish.find_element(
                        by=By.TAG_NAME, value='h2').text
                    dish_image = dish.find_element(
                        by=By.TAG_NAME, value='img').get_attribute("src")
                    dish_price = dish.find_element(
                        by=By.CLASS_NAME, value='current-price').text
                    dish_price = re.sub('[^0-9]', '', dish_price)

                    dish_writer.writerow({dish_headers[0]: dish_id, dish_headers[1]: seller_id, dish_headers[2]: category_id,
                                         dish_headers[3]: dish_name, dish_headers[4]: dish_price, dish_headers[5]: dish_image})
                    print(dish_name)
                    # print(dish_image)
                    # print(dish_price)
                    # print(category_id, seller_id, dish_id)
                    dish_id += 1
                seller_id += 1
                seller_index += 1
                time.sleep(1)
                driver.back()
                time.sleep(3)
                sellers = wait.until(find_sellers)
            page_index += 1
            pages = wait.until(find_pages)
            time.sleep(1)
        except Exception as e:
            print(e)
            pages = wait.until(find_pages)
    driver.back()
    time.sleep(3)
    categories = wait.until(find_category)
    category_id += 1
driver.close()
