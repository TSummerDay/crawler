import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from driver.driver import Driver
from utils.serialization import save_file


class ZLibrary:
    def __init__(self, config, url="https://singlelogin.me") -> None:
        self._driver = Driver()
        self._url = url
        self._url_login = "https://singlelogin.me/rpc.php"
        self._config = config
        self._inter_time = None
        self._path = "./data"

    def open_page(self):
        self._driver.get(self._url)
        time.sleep(1)

    def close_page(self):
        self._driver.close()

    def reload(self):
        self.close_page()
        self._driver = Driver()
        self.open_page()
        self.login()

    def back_search_page(self):
        pass

    def login(self):
        self._cookie = requests.post(url=self._url_login, json={"isModal": True,
                                                                "email": self._config['email'],
                                                                "password": self._config['password'],
                                                                "site_mode": "books",
                                                                "action": "login",
                                                                "redirectUrl": None,
                                                                "isSinglelogin": 1,
                                                                "gg_json_mode": 1})
        print(self._cookie)

        WebDriverWait(self._driver, 100).until(EC.presence_of_element_located(
            (By.XPATH, '''/html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/div[1]/input'''))).send_keys(self._config['email'])
        WebDriverWait(self._driver, 100).until(EC.presence_of_element_located(
            (By.XPATH, '''/html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/div[2]/input'''))).send_keys(self._config['password'])
        time.sleep(1)
        # click the sign in button
        # /html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/button
        WebDriverWait(self._driver, 100).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/button"))).click()
        time.sleep(5)

    def search(self, theme: str, search_type: str):
        if search_type == 'article':
            # article search
            WebDriverWait(self._driver, 100).until(EC.presence_of_element_located(
                (By.XPATH, '''//*[@id="colorBoxes"]/ul/li[2]/a'''))).click()
            time.sleep(2)
        # //*[@id="searchFieldx"]
        # 清楚输入框
        WebDriverWait(self._driver, 100).until(EC.presence_of_element_located(
            (By.XPATH, '''//*[@id="searchFieldx"]'''))).clear()
        # 输入查找内容
        WebDriverWait(self._driver, 100).until(EC.presence_of_element_located(
            (By.XPATH, '''//*[@id="searchFieldx"]'''))).send_keys(theme)
        time.sleep(1)

        WebDriverWait(self._driver, 100).until(EC.presence_of_element_located(
            (By.XPATH, '''//*[@id="searchForm"]/div[1]/div/div[2]/div/button'''))).click()
        time.sleep(3)

    def find_book(self, theme: str, type: str):
        cnt = 0
        while True:
            cnt += 1
            name_item = str(cnt*2)
            book_name_str = f'''//*[@id="searchResultBox"]/div[{name_item}]/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/h3/a'''
            file_type_str = f'''//*[@id="searchResultBox"]/div[{name_item}]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[2]/div[3]/a'''
            # //*[@id="searchResultBox"]/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[2]/div[3]/a
            book_name = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, book_name_str))).text
            file_type = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, file_type_str))).text

            if not str(book_name) in theme:
                return False

            if ('pdf' in str(file_type).lower() and type == 'pdf') or type in str(file_type).lower():
                WebDriverWait(self._driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, book_name_str))).click()
                time.sleep(3)
                return True

            if type in ['epub', 'txt'] and 'epub' in str(file_type).lower():
                WebDriverWait(self._driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, book_name_str))).click()
                time.sleep(3)
                return True

    def download(self, theme, type: str):
        # download btn
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div
        # 下拉框 btn
        # 下载button
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a
        # 点击下拉框
        WebDriverWait(self._driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="btnCheckOtherFormats"]'''))).click()
        time.sleep(2)
        cnt = 0
        while True:
            cnt += 1
            item = str(cnt)
            item_str = f'/html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[{item}]'
            href = href = WebDriverWait(self._driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '''/html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a'''))).get_attribute('href')
            try:
                text = WebDriverWait(self._driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, item_str))).text
                if type in str(text).lower():
                    # https://lib-uawgyukaanrjiasfrp4e4wve.late.re/dl/5241666/fb8f77
                    # https://lib-uawgyukaanrjiasfrp4e4wve.late.re/dl/5241666/fb8f77?convertedTo=epub
                    href = f'{href}?convertedTo={type}'
                    res = requests.get(href, headers={})
                    save_file(self._path, res, theme, type)
                    return True
                if 'rtf' in str(text).lower():
                    res = requests.get(href)
                    save_file(self._path, res, theme, type)
                    return True
            except Exception as e:
                print(e)
                return False
            # //*[@id="btnCheckOtherFormats"]
            # 第一个
            # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[1]/a
            # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[2]
            # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[3]/a
            # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[4]/a
