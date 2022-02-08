import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
# from selenium.webdriver.support import expected_conditions as EC, wait

username = 'z8468426'
password = 'jiang717900150'
longitude = '117.242693'
latitude = '29.320587'
max_attempts = 5
SCKEY = "SCT115169TieTo42L8L9elY5Q7RiAujYJF"


def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('disable-gpu')
    service = Service(executable_path='d:/chrome_driver/chromedriver.exe')
    browser = webdriver.Chrome(service=service, options=options)
    return browser


def login(browser, username, password, el_user, el_pwd, el_btn):
    username_input = browser.find_element(By.XPATH, el_user)
    password_input = browser.find_element(By.XPATH, el_pwd)
    login_button = browser.find_element(By.XPATH, el_btn)
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()
    time.sleep(5)
    # wait.WebDriverWait(browser, 5).until(EC.title_contains('个人中心'))


def report(browser, longitude, latitude, el_in, el_loc, el_sub, el_con):
    js_code = f'''
window.navigator.geolocation.getCurrentPosition = function (success) {{
  let position = {{
    coords: {{
      longitude: "{longitude}",
      latitude: "{latitude}",
    }},
  }};
  success(position);
}};
    '''
    browser.execute_script(js_code)
    in_school_button = browser.find_element(By.XPATH, el_in)
    in_school_button.click()
    time.sleep(2)

    location_button = browser.find_element(By.XPATH, el_loc)
    location_button.click()
    time.sleep(2)

    # wait.WebDriverWait(browser, 5).until(lambda _: location_button.get_attribute('value'))
    submit_button = browser.find_element(By.XPATH, el_sub)
    submit_button.click()
    try:
        confirm_button = browser.find_element(By.XPATH, el_con)
        confirm_button.click()
        time.sleep(2)
        msg = str(datetime.date.today()) + ' 健康打卡成功'
    except Exception as e:
        msg = str(datetime.date.today()) + ' 健康打卡失败\n' + str(e)
    return msg
    # wait.WebDriverWait(browser, 5).until(EC.visibility_of_element_located([By.XPATH, el_con]))
    # wait.WebDriverWait(browser, 5).until_not(EC.element_to_be_clickable(submit_button))


def msg2wechat(msg):
    payload = {'text': msg}
    requests.get(f"https://sc.ftqq.com/{SCKEY}.send", params=payload)


if __name__ == "__main__":
    with open('meta.json', 'r') as fp:
        meta = json.load(fp)
    print('meta data is: ', meta)

    attempts = 0
    while attempts <= max_attempts:
        attempts += 1
        print('-' * 20 + f'the {attempts:3} th attempt' + '-' * 20)

        browser = driver()
        browser.implicitly_wait(30)

        print('open login page...')
        browser.get(meta['url']['login'])
        print(browser.title, browser.current_url)
        print('login page opened')

        print('login into system...')
        login(
            browser,
            username,
            password,
            meta['el']['username_input'],
            meta['el']['password_input'],
            meta['el']['login_btn'],
        )
        print('login succeeded')

        print('open report page...')
        browser.get(meta['url']['report'])
        print(browser.title, browser.current_url)
        print('report page opened')

        print('start reporting...')
        message = report(
            browser,
            longitude,
            latitude,
            meta['el']['in_school_button'],
            meta['el']['location_button'],
            meta['el']['submit_button'],
            meta['el']['confirm_button'],
        )
        print('report succeeded')

        break

    msg2wechat(message)
    print('message has been sent to wechat!')
    browser.quit()
    print('task finished successfully!')
