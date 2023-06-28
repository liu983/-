from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from chaojiying import Chaojiying_Client
from selenium.webdriver.common.keys import Keys
import time

'''本项目中使用的time.sleep()大部分可以替换为selenium的显示等待，可以提升爬取效率，减少等待时间 '''

def main():
   
    option = Options()
  
    option.add_argument(' --disable-blink-features=AutomationControlled')
    # 输入公司名
    company_name = input("输入要查询的公司名称 例 华为技术有限公司: ")
    web = Chrome(options=option)


    # 进入天眼查主页
    web.get('https://www.tianyancha.com/')
    time.sleep(2)
    # 1.进行登录并获取cookies
    cookies = auto_login(web)
    # 将cookie加入到浏览器中
    web.add_cookie(cookies)

    # 2.获取输入公司名的所有专利信息数据,并输出
    get_data(company_name, web)


# 传入Chrome实例对象web,自动登录获取cookie并将其返回
# 怪物吃了拼图需要再次滑块验证
def auto_login(web):
    
    # 点击登录
    web.find_element_by_xpath('//*[@id="page-container"]/div[1]/div/div[1]/div[2]/div/div[5]').click()
    # 点击账号密码登录
    web.find_element_by_xpath('//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[2]').click()
    # 选择密码登录
    web.find_element_by_xpath(
        '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]').click()

    # 输入用户名
    web.find_element_by_xpath(
        '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/div[1]/input').send_keys(
        '天眼查账号')
    # 输入密码
    web.find_element_by_xpath(
        '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/input').send_keys(
        '天眼查密码')
    # 勾选协议复选框
    web.find_element_by_xpath(
        '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[3]/input').click()
    # 点击登录
    web.find_element_by_xpath(
        '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/button').click()
    time.sleep(2)
    
    # 注意：获取偏移量及滑块验证整个流程应当放在循环中，验证通过跳出循环（本demo未使用）
    
    # 点击滑块获取完整拼图
    hk = web.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div[2]')
    hk.click()
    time.sleep(5)
    # 获取验证码图片(返回字节流图片)
    img = web.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/a[2]').screenshot_as_png
    # 初始化超级鹰并调用超级鹰api获取坐标
    chaojiying = Chaojiying_Client('超级鹰账号', '超级鹰密码', '软件ID')
    dic = chaojiying.PostPic(img, 9101)
    result = dic['pic_str']
    rs_list = result.split("|")
    for rs in rs_list:
        p_temp = rs.split(",")
        x = int(p_temp[0])
        print(f"x的坐标为:{x}")
        y = int(p_temp[1])
        print(f"y的坐标为:{y}")
        action = ActionChains(web)
        # 鼠标点击滑块不释放并向右滑动x-35个像素点后释放鼠标,35为滑块宽带的一半
        action.click_and_hold(hk).move_by_offset(x-35, 0).release().perform()
        print('拖动完成')
        break

    # 获取登录成功后的 Cookie
    cookies = web.get_cookies()
    return cookies


# 获取传入公司的专利信息数据,并打印在控制台
def get_data(company_name, web):
    # 在搜索框中输入公司名并回车进行搜索
    web.find_element_by_xpath('//*[@id="page-container"]/div[1]/div/div[3]/div[2]/div[1]/div[1]/input').send_keys(
        company_name, Keys.ENTER)
    # 点击进入公司详情页
    web.find_element_by_xpath(
        '//*[@id="page-container"]/div/div[2]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/a/span/em').click()

    # 切换至新窗口
    web.switch_to.window(web.window_handles[-1])
    time.sleep(5)
    # 点击知识产权，查看专利信息
    zl = web.find_element_by_xpath('//*[@id="JS_Layout_Nav"]/div/div/div/div/div[1]/div[6]/a')
    time.sleep(3)
    act = ActionChains(web)
    act.double_click(zl).perform()

    # 循环选择页码获取专利信息数据
    while True:
        table = web.find_elements_by_class_name('table-wrap')
        # 获取当前页所有专利信息
        tr_all = table[2].find_elements_by_xpath('./tbody/tr')
        # print(len(tr_all))

        # 解析数据
        for tr in tr_all:
            # "序号", "申请日", "专利名称", "专利类型", "专利状态", "申请号", "公开（公布号）", "公开（公告日）", "发明人"
            # print(tr.text)
            xuhao = tr.find_element_by_xpath('./td[1]').text
            print('序号：' + xuhao)
            sqr = tr.find_element_by_xpath('./td[2]').text
            print('申请日：' + sqr)
            zlmc = tr.find_element_by_xpath('./td[3]').text
            print('专利名称：' + zlmc)
            zllx = tr.find_element_by_xpath('./td[4]').text
            print('专利类型：' + zllx)
            zlzt = tr.find_element_by_xpath('./td[5]').text
            print('专利状态：' + zlzt)
            sqh = tr.find_element_by_xpath('./td[6]').text
            print('申请号：' + sqh)
            gbh = tr.find_element_by_xpath('./td[7]').text
            print('公开（公布号）：' + gbh)
            ggr = tr.find_element_by_xpath('./td[8]').text
            print('公开（公告日）：' + ggr)
            fmr = tr.find_element_by_xpath('./td[9]').text
            print('发明人：' + fmr)
            print()

        # 点击下一页
        try:
            web.find_element_by_xpath(
                '//*[@id="page-root"]/div[3]/div[1]/div[3]/div/div[2]/div[2]/div/div[3]/div/div/div[4]/div/div/div/div/div[13]')
            time.sleep(2)
        except:
            # 找不到该元素说明到最后一页了退出循环
            break


if __name__ == '__main__':
    main()
