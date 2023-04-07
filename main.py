from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

account = ('账号', '密码')

url = 'http://jyjxxt.yjs.suda.edu.cn/'
driver = webdriver.Chrome()
driver.get(url)


def login():
    # 登录
    driver.find_element_by_id('btnlogin_tysf').click()  # 选择统一验证登录
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
    # 培养环境管理
    pyhjdj = 'http://jyjxxt.yjs.suda.edu.cn/(S(r21jjohhwdhhl1gd2d3m3hjp))/student/pygl/pyhjdj'
    driver.get(pyhjdj)

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


# 科研成果


login()

# 读取学术会议数据
import pandas
df = pandas.read_csv('学术报告.csv')
df = df[df['学工号'] == account[0]]
for row_id, row in df.iterrows():
    add_research_activity(name=row['会议名称'], date=row['打卡时间'].split(' ')[0])
    # break

driver.close()
