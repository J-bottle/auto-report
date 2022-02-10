import argparse
import json
import time
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

max_attempts = 3

def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    service = Service(executable_path=ChromeDriverManager(log_level=0).install())
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


def msg2wechat(msg):
    payload = {'text': msg}
    requests.get(f"https://sc.ftqq.com/{SCKEY}.send", params=payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My health-report automatic program.')
    parser.add_argument('--username', '-u', type=str, help='username')
    parser.add_argument('--password', '-p', type=str, help='password')
    parser.add_argument('--longitude', '-o', type=float, help='longitude')
    parser.add_argument('--latitude', '-a', type=float, help='latitude')
    parser.add_argument('--SKY', '-s', type=str, help='KEY used to send message to wechat.')
    opt = parser.parse_args()

    with open('meta.json', 'r') as fp:
        meta = json.load(fp)

    attempt = 0

    while attempt <= max_attempts:
        attempt += 1
        print('-' * 20 + f'the {attempt:3} th attempt' + '-' * 20)

        browser = driver()
        browser.implicitly_wait(30)  # 隐式等待，检索每个元素都会最多等待的时间

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
