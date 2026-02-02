from selenium import webdriver
from selenium.webdriver.common.by import By
from time import  sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#переходим в контакты
browser = webdriver.Chrome()
browser.get('https://saby.ru/')
dropdown_butt = browser.find_element(By.CLASS_NAME, 'sbisru-Header__menu-item-1')
dropdown_butt.click()
sleep(1)
click_butt = browser.find_element(By.LINK_TEXT, 'Еще 13 офисов в регионе')
click_butt.click()
sleep(1)

#кликаем на баннер
logo = browser.find_element(By.CLASS_NAME, 'sbisru-Contacts__logo-tensor')
logo.click()
sleep(2)

#проверка наличия блока о людях
browser.switch_to.window(browser.window_handles[1])
def is_text_present():
    try:
        # Ожидание появления элемента (до 10 секунд)
        xpath = "//p[text()='Сила в людях']"

        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except:
        return False
if is_text_present():
    link_xpath = "//p[text()='Сила в людях']/ancestor::div[contains(@class, 'tensor_ru-Index__card')]//a[text()='Подробнее']"
    about_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, link_xpath))
    )
    about_btn.click()
    sleep(1)
else:
    print('Не нажалось "Подробнее"')

#проверка размеров изображений
images = browser.find_elements(By.CLASS_NAME, 'tensor_ru-About__block3-image')
assert len(images) == 4, f"ожидалось 4 картинки, нашлось {len(images)}"

first_image = images[0].size
stand_h = first_image['height']
stand_w = first_image['width']

errors =[]
for i, img in enumerate(images):
    cur_size = img.size
    w = cur_size['width']
    h = cur_size['height']

    if stand_h != h or stand_w != w:
        errors.append(f"изображение {i+1} имеет нестандартный размер")
if not errors:
    print('все изображения одинакового размера')
else:
    for error in errors:
        print(error)



