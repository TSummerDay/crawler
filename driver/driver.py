import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import requests


def Driver():
    # get直接返回，不再等待界面加载完成
    # desired_capabilities = DesiredCapabilities.EDGE
    # desired_capabilities["pageLoadStrategy"] = "none"

    # 设置 Edge 驱动器的环境
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 设置 Edge 不加载图片，提高速度
    # options.add_experimental_option(
    #     "prefs",   {"profile.managed_default_content_settings.images": 2})

    # 创建一个 Edge 驱动器
    driver = webdriver.Chrome(options=chrome_options)

    return driver
