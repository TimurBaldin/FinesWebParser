import random
from typing import Any
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import repository
from classes import BrowserType
from selenium import webdriver
from db.tables import FineDetails


def parser(type: BrowserType, car_details_list):
    browser = get_browser(type)

    browser.delete_all_cookies()
    browser.get('https://xn--90adear.xn--p1ai/check/fines')

    is_first = True

    for car in car_details_list:

        if car.get_img_data() is not None:
            continue

        timeout_ex = False
        action_element('checker', browser, 60)

        if is_first is False:
            clear_text(browser.find_element_by_name('regnum'))
            clear_text(browser.find_element_by_name('regreg'))
            clear_text(browser.find_element_by_name('stsnum'))

        browser.find_element_by_name('regnum').send_keys(car.reg_num)
        browser.find_element_by_name('regreg').send_keys(car.reg_reg)
        browser.find_element_by_name('stsnum').send_keys(car.sts_num)

        checker = browser.find_element_by_class_name('checker')
        time.sleep(random.randint(1, 3))
        checker.click()

        start_time = time.time()
        while True:
            try:
                action_element("camera-img-btn", browser, 1)
                break
            except TimeoutException:
                try:
                    action_element("close_modal_window", browser, 1)
                    browser.find_element_by_class_name('close_modal_window').click()
                    continue
                except TimeoutException:
                    if int(time.time() - start_time) >= 15:
                        print('Сработал таймаут --- refresh')
                        browser.refresh()
                        timeout_ex = True
                        car.decrement()
                        break
                    continue

        if car.get_count() == 0:
            print('Данные по реквезитам не были получены ')
            browser.quit()
        elif timeout_ex:
            car_details_list.append(car)
            continue

        car.set_img_data(
            parser_camera_img(browser.find_elements_by_class_name('camera-img-btn'), browser, car.get_id())
        )

        is_first = False
        browser.refresh()

    browser.quit()
    return car_details_list


def clear_text(element):
    element.clear()
    length = len(element.get_attribute('value'))
    element.send_keys(length * Keys.BACKSPACE)


def save_pic(browser, fine_id)->list:
    pics=list()
    for pic in BeautifulSoup(browser.page_source, 'html5lib').find_all('img', attrs={"class": "cafap-photo-img"}):
        str_pic = pic.__str__()
        base64_pic = str_pic[str_pic.find(',/') + 1:len(str_pic) - 3]
        pics.append(base64_pic)
        repository.save_img(fine_id=fine_id, img=base64_pic)

    return pics


def get_browser(type: BrowserType) -> Any:
    if BrowserType.SELENOID is type:
        capabilities = {
            "browserName": "firefox",
            "version": "84",
            "platform": "LINUX",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            }
        }
        return webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=capabilities
        )
    if BrowserType.FIREFOX is type:
        chromedriver = '/usr/local/Cellar/geckodriver'
        return webdriver.Firefox(chromedriver)


def action_element(value: str, browser: object, time_wait: int) -> Any:
    return WebDriverWait(browser, time_wait).until(
        EC.visibility_of_element_located((By.CLASS_NAME, value)))


def parser_camera_img(elements, browser, car_id):
    fines_details = save_fines(browser=browser, car_id=car_id)
    index = 0
    pics_list = list()
    for element in elements:
        try:
            element.click()
            action_element("cafap-photo-img", browser, 15)
            pics_list.append(save_pic(browser, fine_id=fines_details[index]))
            index += 1
        except TimeoutException:
            print("Данные по элементу не были получены ")
            pics_list.append(list("Фотоматериалы не были получены"))
            continue

    return pics_list


def save_fines(browser, car_id):
    fines_details = list()
    for element in browser.find_elements_by_class_name('finesItem'):
        fines_details.append(FineDetails(car_id=car_id, fine_description=element.text))
    repository.save_fines(fines_details)
    return fines_details





