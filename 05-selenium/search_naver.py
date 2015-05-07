import os
import sys
from getpass import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main(id, password, browser):
    if browser == 'ie':
        ie_driver = os.path.abspath('IEDriverServer_win32_2.45.0.exe')
        driver = webdriver.Ie(ie_driver)
    elif browser == 'chrome':
        if sys.platform == 'darwin':
            chrome_driver = os.path.abspath('chromedriver_mac_32')
        elif sys.platform.startswith('win'):
            chrome_driver = os.path.abspath('chromedriver_win_32.exe')
        else:
            exit('not found chrome-driver for {}'.format(sys.platform))
        driver = webdriver.Chrome(chrome_driver)
    else:
        exit('invalid browser : {}'.format(browser))

    driver.get('https://nid.naver.com/nidlogin.login')

    element = driver.find_element_by_name('id')
    element.send_keys(id)

    element = driver.find_element_by_name('pw')
    element.send_keys(password)

    element.send_keys(Keys.RETURN)

    # print('3초 뒤에 브라우저를 닫습니다.')
    # sleep(3)
    # driver.close()


def exit(message):
    print(message, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    try:
        browser = sys.argv[1].lower()
    except IndexError:
        exit('사용법> {} 브라우저<ie/chrome>'.format(sys.argv[0]))

    id = input('네이버 아이디 : ')
    if not id:
        exit('아이디를 입력해주세요.')

    password = getpass('네이버 비밀번호 : ')
    if not password:
        exit('암호를 입력해주세요.')

    main(id, password, browser)

