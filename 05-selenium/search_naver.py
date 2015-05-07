import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main(browser):
    if browser == 'ie':
        ie_driver = os.path.abspath('IEDriverServer_win32_2.45.0.exe')
        driver = webdriver.Ie(ie_driver)
    elif browser == 'chrome':
        if sys.platform == 'darwin':
            chrome_driver = os.path.abspath('chromedriver_mac_32')
        elif sys.platform.startswith('win'):
            chrome_driver = os.path.abspath('chromedriver_win_32.exe')
        else:
            print('not found chrome-driver for {}'.format(sys.platform), file=sys.stderr)
            sys.exit(1)
        driver = webdriver.Chrome(chrome_driver)
    else:
        print('invalid browser : {}'.format(browser), file=sys.stderr)
        sys.exit(1)

    driver.get('http://naver.com')

    element = driver.find_element_by_name("query")
    element.send_keys("파이썬")
    element.send_keys(Keys.RETURN)

    print('3초 뒤에 브라우저를 닫습니다.')
    sleep(3)
    driver.close()


if __name__ == '__main__':
    try:
        browser = sys.argv[1].lower()
    except IndexError:
        print('사용법> {} 브라우저<ie/chrome>'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    main(browser)

