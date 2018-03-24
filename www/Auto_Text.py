from selenium import webdriver

Base_url='http://127.0.0.1:9000/register'
def text():
    driver=webdriver.Chrome('C:/Users/llx/Desktop/chromedriver.exe')
    driver.get(Base_url)
    driver.find_element_by_id('name').send_keys('asd1')
    driver.find_element_by_id('email').send_keys('asdf1@qq.com')
    driver.find_element_by_id('password1').send_keys('123456')
    driver.find_element_by_id('password2').send_keys('123456')
    driver.find_element_by_id('submmit').click()
