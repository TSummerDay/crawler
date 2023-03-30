import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def open_page(driver, theme, url="https://kns.cnki.net/kns8/AdvSearch"):
    #
    driver.get(url)
    time.sleep(2)

    #
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, '''//*[@id="gradetxt"]/dd[3]/div[2]/input'''))).send_keys(theme)
    time.sleep(2)

    # click search
    WebDriverWait(driver, 100).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input"))).click()
    time.sleep(3)

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


def crawl(driver, papers_need, theme, count=1):
    # 当爬取数量小于需求时，循环网页页码
    while count <= papers_need:
        # 等待加载完全，休眠3S
        time.sleep(3)

        title_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "fz14")))
        # 循环网页一页中的条目
        for i, _ in enumerate(title_list):
            try:
                if count % 20 != 0:
                    term = count % 20  # 本页的第几个条目
                else:
                    term = 20
                title_xpath = f"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr[{term}]/td[2]"
                author_xpath = f"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr[{term}]/td[3]"
                source_xpath = f"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr[{term}]/td[4]"
                date_xpath = f"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr[{term}]/td[5]"
                database_xpath = f"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr[{term}]/td[6]"
                title = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, title_xpath))).text
                authors = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, author_xpath))).text
                source = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, source_xpath))).text
                date = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, date_xpath))).text
                database = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, database_xpath))).text
                # 点击条目
                title_list[i].click()
                # 获取driver的句柄
                n = driver.window_handles
                # driver切换至最新生产的页面
                driver.switch_to.window(n[-1])
                time.sleep(3)
                # 开始获取页面信息
                title = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h1"))).text
                authors = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h3[1]"))).text
                institute = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h3[2]"))).text
                abstract = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "abstract-text"))).text
                try:
                    keywords = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "keywords"))).text[:-1]
                    cssci = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/a[2]"))).text
                except:
                    keywords = '无'
                    cssci = 'NULL'
                url = driver.current_url

                # 写入文件
                res = f"{count}\t{title}\t{authors}\t{cssci}\t{institute}\t{date}\t{source}\t{database}\t{keywords}\t{abstract}\t{url}".replace(
                    "\n", "") + "\n"
                print(res)
                with open(f'{theme}.tsv', 'a', encoding='gbk') as f:
                    f.write(res)
            except:
                print(f" 第{count} 条爬取失败\n")
                # 跳过本条，接着下一个
                continue
            finally:
                # 如果有多个窗口，关闭第二个窗口， 切换回主页
                n2 = driver.window_handles
                if len(n2) > 1:
                    driver.close()
                    driver.switch_to.window(n2[0])
                # 计数,判断篇数是否超出限制
                count += 1
        if count == papers_need:
            break
        else:
            # 切换到下一页
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//a[@id='PageNext']"))).click()


def webserver(theme):
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

    # 设置所需篇数
    papers_need = 50

    res_unm = int(open_page(driver, theme))

    # 判断所需是否大于总篇数
    papers_need = papers_need if (papers_need <= res_unm) else res_unm
    return driver, papers_need, theme


if __name__ == "__main__":
    # 输入需要搜索的内容
    theme = input("请输入你要搜索的期刊名称：")
    # theme = "管理科学学报"
    driver, papers_need, theme = webserver(theme)
    crawl(driver, papers_need, theme)
    # 关闭浏览器
    driver.close()
