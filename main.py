from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import argparse
import pandas

account = ('账号', '密码')

url = 'http://jyjxxt.yjs.suda.edu.cn/'
driver = webdriver.Chrome()
driver.get(url)

xpaths = {
    '培养环节管理': '//*[@id="nav_box"]/div[2]/ul/li[14]/a',
    '培养环节管理-学术活动': '//*[@id="tabs"]/div[1]/div[3]/ul/li[1]/a',
}


def login():
    # 登录
    driver.find_element_by_id('btnlogin_tysf').click()  # 选择统一身份认证登录
    driver.find_element_by_id('username').send_keys(account[0])  # 输入账号
    driver.find_element_by_id('password').send_keys(account[1])  # 输入密码
    driver.find_element_by_id('login-submit').click()  # 点击登录


def add_research_activity(name, speaker='无', department='苏州大学', location='会议室', date='2023-04-01',
                          summary='无'):
    '''
    新增单个学术活动
    :param name: 活动名称
    :param speaker: 主讲人
    :param department: 主办单位
    :param location: 地点
    :param date: 日期（默认愚人节）
    :param summary: 总结
    :return: 无返回值
    '''
    data = [name, speaker, department, location, date, summary]
    # 培养环节管理
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['培养环节管理'])))
    driver.find_element_by_xpath(xpaths['培养环节管理']).click()
    # url = driver.find_element_by_xpath(xpaths['培养环节管理']).get_property('href')
    # driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btn_add10")))  # 等待页面加载
        driver.find_element_by_id('btn_add10').click()  # 新增 学术活动
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtnr0")))  # 等待页面加载
        for i, d in enumerate(data):
            if i == 4:
                # 时间输入特殊处理
                ele = driver.find_element_by_xpath(
                    '// *[ @ id = "dg"] / tbody / tr[5] / td[2] / span / input[1]')  # 定位时间输入框
            else:
                ele = driver.find_element_by_id(f'txtnr{i}')  # 定位文本输入框
            ele.send_keys(data[i])  # 输入内容
            if i == 4:
                # 时间输入需要在日历控件出现后，额外输入一个回车
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div[2]/table/tbody/tr/td[2]/a")))  # 等待日历控件加载
                ele.send_keys(Keys.ENTER)  # 输入回车
        driver.find_element_by_id('btnsave').click()  # 保存 学术活动
    except Exception:
        driver.quit()


def clear_research_activities():
    '''
    清空所有学术活动
    :return: 无返回值
    '''
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['培养环节管理'])))
    driver.find_element_by_xpath(xpaths['培养环节管理']).click()
    # url = driver.find_element_by_xpath(xpaths['培养环节管理']).get_property('href')
    # driver.get(url)
    try:
        # 等待数据加载（已录入的数据多时加载很慢
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="10-1"]/div/div[2]/div/div/div[2]/div[1]/div/table/tbody/tr/td[2]/div')))
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="10-1"]/div/div[2]/div/div/div[2]/div[2]/table/tbody')))
        rows = driver.find_elements_by_xpath('//tbody/tr[contains(@id,"datagrid-row")]')

        for i in range(len(rows)//2):
            # 只能每次删除一行（即使多选也没用，系统不支持
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="10-1"]/div/div[2]/div/div/div[2]/div[1]/div/table/tbody/tr/td[2]/div')))
            first_row_xpath = '//*[@id="datagrid-row-r1-2-0"]//input'
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, first_row_xpath)))
            driver.find_element_by_xpath(first_row_xpath).click()
            driver.find_element_by_id('btn_del10').click()
            break
    except Exception:
        driver.quit()

    # 科研成果


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user_name', type=str, default='', help='学号')
    parser.add_argument('-p', '--password', type=str, default='', help='学号')
    args = parser.parse_args()
    account = (args.user_name, args.password)
    login()

    # 清空学术会议列表
    # clear_research_activities()

    # 读取学术会议数据
    df = pandas.read_csv('学术报告.csv')
    df = df[df['学工号'] == account[0]]
    for row_id, row in df.iterrows():
        add_research_activity(name=row['会议名称'], date=row['打卡时间'].split(' ')[0])
        # break

    driver.close()
