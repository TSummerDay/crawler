import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests


def open_page(driver, url="https://singlelogin.me"):
    #
    driver.get(url)
    time.sleep(2)


def other():
    # click to exchange mode for Chinese literature search
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[1]/div/div/div/a[1]"))).click()
    time.sleep(3)

    # acquire the total number of literatures and pages
    res_num = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[2]/form/div/div[1]/div[1]/span[1]/em"))).text

    # Remove commas in the thousandth place
    res_num = int(res_num.replace(",", ''))
    page_num = int(res_num / 20) + 1
    print(f"共找到 {res_num} 条结果， {page_num}页。")
    return res_num


def login(driver, user, password):
    # try:
    #     WebDriverWait(driver, 100).until(EC.presence_of_element_located(
    #         (By.XPATH, "/html/body/table/tbody/tr[2]/td/div/div/div/div[1]/div[2]/div[2]/form/button"))).click()
    #     time.sleep(2)
    # except Exception as e:
    # user
    # /html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/div[1]/input
    # password
    # /html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/div[2]/input
    # enter the password
    print("first login")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, '''/html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/div[1]/input'''))).send_keys(user)
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, '''/html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/div[2]/input'''))).send_keys(password)
    time.sleep(1)
    # click the sign in button
    # /html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/button
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/table/tbody/tr[2]/td/div/div/div/div/div[1]/form/button"))).click()
    time.sleep(3)


def crawl(driver, theme, type="pdf"):
    find_book(driver, theme, type)
    download(driver)


def search(driver, theme, type="book"):
    if type == "article":
        # article search
        WebDriverWait(driver, 100).until(EC.presence_of_element_located(
            (By.XPATH, '''//*[@id="colorBoxes"]/ul/li[2]/a'''))).click()
        time.sleep(2)

    # //*[@id="searchFieldx"]
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, '''//*[@id="searchFieldx"]'''))).send_keys(theme)
    time.sleep(2)
    # click the search button//*[@id="searchForm"]/div[1]/div/div[2]/div/button
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, '''//*[@id="searchForm"]/div[1]/div/div[2]/div/button'''))).click()
    time.sleep(5)


def find_book(driver, theme: str, type='pdf'):
    cnt = 0
    while True:
        cnt += 1
        name_item = str(cnt*2)
        book_name_str = f'''//*[@id="searchResultBox"]/div[{name_item}]/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/h3/a'''
        file_type_str = f'''//*[@id="searchResultBox"]/div[{name_item}]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[2]/div[3]/a'''
        # //*[@id="searchResultBox"]/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[2]/div[3]/a
        book_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, book_name_str))).text
        file_type = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, file_type_str))).text

        if not str(book_name) in theme:
            return False

        if ('pdf' in str(file_type).lower() and type == 'pdf') or type in str(file_type).lower():
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, book_name_str))).click()
            time.sleep(3)
            return True

        if type in ['epub', 'txt'] and 'epub' in str(file_type).lower():
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, book_name_str))).click()
            time.sleep(3)
            return True
        # author
        # //*[@id="searchResultBox"]/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div[2]/a
        # //*[@id="searchResultBox"]/div[4]/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div[2]/a
        # //*[@id="searchResultBox"]/div[4]/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div[2]
        # //*[@id="searchResultBox"]/div[6]/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/a
        # the button 下拉框
        # //*[@id="btnCheckOtherFormats"]

        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[4]/a
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[5]/a
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[6]/a
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[7]/a

        # button /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a
        # type /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a/span


def download(driver, type='pdf'):
    # download btn
    # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div
    # 下拉框 btn
    # 下载button
    # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a
    # 点击下拉框
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '''//*[@id="btnCheckOtherFormats"]'''))).click()
    time.sleep(2)
    cnt = 0
    while True:
        cnt += 1
        item = str(cnt)
        item_str = f'/html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[{item}]'
        href = href = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '''/html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a'''))).get_attribute('href')
        try:
            text = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, item_str))).text
            if type in str(text).lower():
                # https://lib-uawgyukaanrjiasfrp4e4wve.late.re/dl/5241666/fb8f77
                # https://lib-uawgyukaanrjiasfrp4e4wve.late.re/dl/5241666/fb8f77?convertedTo=epub
                href = f'{href}?convertedTo={type}'
                reponse = requests.get(href)
                return True
            if 'rtf' in str(text).lower():
                reponse = requests.get(href)
                break
        except Exception as e:
            print(e)
            return False
        # //*[@id="btnCheckOtherFormats"]
        # 第一个
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[1]/a
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[2]
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[3]/a
        # /html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul/li[4]/a


def webserver(config):
    # get直接返回，不再等待界面加载完成
    desired_capabilities = DesiredCapabilities.EDGE
    desired_capabilities["pageLoadStrategy"] = "none"

    # 设置 Edge 驱动器的环境
    options = webdriver.EdgeOptions()
    # 设置 Edge 不加载图片，提高速度
    options.add_experimental_option(
        "prefs",   {"profile.managed_default_content_settings.images": 2})

    # 创建一个 Edge 驱动器
    driver = webdriver.Edge(options=options)

    open_page(driver)
    login(driver, config['user'], config['password'])
    return driver


def load_config():
    config_path = "config.json"
    import json
    f = open(config_path, 'r', encoding='UTF-8')
    config = json.load(f)
    return config


if __name__ == "__main__":
    # 输入需要搜索的内容
    config = load_config()
    theme = "红岩"
    type = "book"
    # theme = "管理科学学报"
    driver = webserver(config)
    search(driver, theme, type)
    crawl(driver, theme)
    # 关闭浏览器
    driver.close()
