from selenium import webdriver
from PIL import Image
import os,time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
from time import sleep
from PIL import Image
from VerifyCodeCNN import CNN
import datatest
import requests
import re
import hashlib
from lxml import etree

MODEL_SAVE_PATH = './data/model.ckpt'
cnn = CNN(1000, 0.0005, MODEL_SAVE_PATH)


username='2017301500258'
password='dingWB0810'
headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",}
codeurl='http://bkjw.whu.edu.cn/servlet/GenImg'
codeurl=''

def getpic(headers=headers):
	global codeurl
	i = 0
	while i < 10:
		try:
			html = requests.get(codeurl, headers = headers,verify=False,timeout=0.3)
			return html
		except requests.exceptions.RequestException:
			i += 1

def get_preinf(url='http://bkjw.whu.edu.cn/',headers=headers):
	global codeurl
	html = requests.get(url, headers = headers,verify=False,timeout=0.3)
	st=html.text
	rule=r'#captcha-img\d'
	captcha=re.findall(rule, st)
	imgp=10
	for ca in captcha:
		num=re.findall(r'\d',ca)
		imgp=imgp-int(num[0])


	html = etree.HTML(html.text)
	action=html.xpath('//*[@id="loginBox"]/form/@action')[0]
	img=html.xpath('//*[@id="captcha-img'+str(imgp)+'"]/@src')[0]
	login='http://bkjw.whu.edu.cn'+action
	codeurl='http://bkjw.whu.edu.cn'+img
	print(codeurl)
	return codeurl



def login():
	driver = webdriver.Firefox()
	driver.get('http://bkjw.whu.edu.cn/')
	i=0
	while driver.current_url!='http://bkjw.whu.edu.cn/stu/stu_index.jsp' and i<10:
		global codeurl
		codeurl=get_preinf()
		valcode = getpic(headers)
		f = open('valcode.png', 'wb')
		f.write(valcode.content)
		f.close()
		driver.delete_cookie('JSESSIONID')
		cookies=driver.get_cookies()
		for cookie in cookies: 
			print(cookie["name"],cookie["value"])
		cookies=requests.utils.dict_from_cookiejar(valcode.cookies)
		print(cookies)
		#driver.delete_all_cookies()
		print(type(cookies))
		driver.add_cookie({"name":"JSESSIONID","value":cookies['JSESSIONID']})
		vcode = datatest.main(cnn)

		sleep(0.1)
		driver.find_element_by_name("id").send_keys(username)
		sleep(0.1)
		driver.find_element_by_name("pwd").send_keys(password)
		sleep(0.1)
		driver.find_element_by_name("xdvfb").send_keys(vcode)
		sleep(0.1)
		driver.find_element_by_id("loginBtn").click()
		sleep(0.1)
	if i<10:
		return 1
	return 0

if __name__ == "__main__":
	login()
