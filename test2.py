from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация браузера
browser = webdriver.Chrome()
browser.maximize_window()


def region_swap(region):

    region_selector = browser.find_element(By.CLASS_NAME, "sbis_ru-Region-Chooser__text")

    browser.execute_script("arguments[0].click();", region_selector)

    # Ждем появления панели выбора
    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "sbis_ru-Region-Panel")))

    # Ищем новый регион
    new_region_locator = (By.XPATH, f"//span[contains(text(), '{region}')]")
    region_option = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(new_region_locator))
    region_option.click()

    # WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "sbis_ru-Region-Chooser__text"), region))
    print(f"Регион успешно изменен на {region}")


try:
    browser.get('https://saby.ru/')

    #  Находим и открываем меню
    dropdown_butt = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'sbisru-Header__menu-item-1'))
    )
    dropdown_butt.click()

    #  Ждем, пока оверлей панели регионов исчезнет
    overlay_selector = (By.CLASS_NAME, 'sbis_ru-Region-Panel__overlay')
    WebDriverWait(browser, 10).until(EC.invisibility_of_element_located(overlay_selector))

    #  ВАЖНО: Заново находим кнопку меню после смены региона
    dropdown_butt = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'sbisru-Header__menu-item-1'))
    )
    dropdown_butt.click()

    #  Кликаем по ссылке "Еще 13 офисов"
    click_butt = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Еще 13 офисов в регионе'))
    )
    click_butt.click()
    print("Успешный переход в список офисов")

finally:
    pass

#проверка региона

def region_check(expected_region):
    region_selector = (By.CLASS_NAME, 'sbis_ru-Region-Chooser__text')
    WebDriverWait(browser, 15).until(
        EC.text_to_be_present_in_element(region_selector, expected_region)
    )
    element = browser.find_element(*region_selector)
    current_region = element.text
    assert current_region == expected_region, f"Ожидался {expected_region}, но определился {current_region}"
    return current_region

try:
    region_check('Ярославская обл.')
    print('Регион совпадает')
except:
    pass


#проверка наличия партнеров
def partners_check_and_count():
    partners_list_selector = (By.CLASS_NAME, "sbisru-Contacts-List__item")
    partners = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(partners_list_selector))
    if len(partners) > 0:
        print(f"Список партнеров найден. Количество записей в видимой области: {len(partners)}")
    else:
        print("Список партнеров пуст")
    return(len(partners))

first_partners = partners_check_and_count()

region_swap('Камчатский край')
sleep(2)
region_check('Камчатский край')
next_partners = partners_check_and_count()
assert first_partners == next_partners, "кол-во партнеров не изменилось"