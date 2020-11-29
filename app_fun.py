import random
from tts_ws import tts
import wave
import pyaudio
import time
from selenium import webdriver
import requests
from dytt import get_movie
from whu import login
import sys
sys.path.append("./tiler")
from tiler import run_demo
import re
import os
import json
import hashlib
import base64
import cv2
import requests
def play_audio_file(fname):
    """Simple callback function to play a wave file. By default it plays
    a Ding sound.

    :param str fname: wave file name
    :return: None
    """
    ding_wav = wave.open(fname, 'rb')
    ding_data = ding_wav.readframes(ding_wav.getnframes())
    audio = pyaudio.PyAudio()
    stream_out = audio.open(
        format=audio.get_format_from_width(ding_wav.getsampwidth()),
        channels=ding_wav.getnchannels(),
        rate=ding_wav.getframerate(), input=False, output=True)
    stream_out.start_stream()
    stream_out.write(ding_data)
    time.sleep(0.2)
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()



def app_joke():
	with open('joke.txt','r') as f:
		lines=f.readlines()
		index = random.sample(range(0,len(lines)),1)
		tts(lines[index[0]])
		play_audio_file('res.wav')

def app_baidu():
	
	browser = webdriver.Chrome()
	browser.get('http://www.baidu.com/')


def app_weather(city):
	rb=requests.get('http://wthrcdn.etouch.cn/weather_mini?city='+city)
	text=''
	try:
		rb=rb.json()
		rb=rb['data']['forecast'][0]
		fengli=re.findall(r'\d',rb['fengli'])
		text='今天'+city+rb['type']+',最'+rb['high']+',最'+rb['low']+',风向'+rb['fengxiang']+',风力'+str(fengli[0])+'级'
		print(text)
	except:
		text='查询失败'
	tts(text)
	play_audio_file('res.wav')

def find_port(num):
	cmd='lsof -i:'+num
	res=os.popen(cmd)
	output=res.readlines()
	ret=[]
	if output:
		for item in output[1:]:
			print(item)
			item=item.strip().split()
			ret.append([item[0],item[1]])
	return ret

def app_movie():
	text=get_movie()
	tts(text)
	play_audio_file('res.wav')




def app_port(num):
	ret=find_port(num)
	text='未找到当前用户进程占用'+num+'端口'
	if ret:
		text=''
		for item in ret:
			text+='程序'+str(item[0])+'占用端口'+num+'其PID为'+str(item[1])
	tts(text)
	play_audio_file('res.wav')


def app_kill_port(num):
	ret=find_port(num)
	text="执行成功"
	cmd="kill -9 "
	if ret:
		for item in ret:
			os.system(cmd+item[1])
	tts(text)
	play_audio_file('res.wav')


def app_whu_login():
	ret=login()
	text="登录成功"
	if(ret==0):
		text="登录失败"
	tts(text)
	play_audio_file('res.wav')


def app_reg_face(id):
	text='请对准摄像头'
	tts(text)
	play_audio_file('res.wav')
	capture = cv2.VideoCapture(0)
	i=10
	ret ,frame = capture.read()
	while i>0:
		ret ,frame = capture.read()
		cv2.imwrite('./pic/'+str(id)+'.jpg',frame)
		i-=1
	capture.release() 
	text='拍摄成功'
	tts(text)
	play_audio_file('res.wav')

def app_log_in(id):
	text='请对准摄像头'
	tts(text)
	play_audio_file('res.wav')
	capture = cv2.VideoCapture(0)
	i=10
	ret ,frame = capture.read()
	while i>0:
		ret ,frame = capture.read()
		cv2.imwrite('./pic/temp.jpg',frame)
		i-=1
	capture.release()
	x_appid = '5e55394d'
	# 接口密钥(webapi类型应用开通人脸比对服务后，控制台--我的应用---人脸比对---相应服务的apikey)
	api_key = '1c47845927066ea9f01187383bdfe6c9'
	# webapi接口地址
	url = 'http://api.xfyun.cn/v1/service/v1/image_identify/face_verification'
	# 组装http请求头
	x_time = str(int(time.time()))
	param = {'auto_rotate': True}
	param = json.dumps(param)
	x_param = base64.b64encode(param.encode('utf-8'))
	m2 = hashlib.md5()
	m2.update(str(api_key + x_time + str(x_param, 'utf-8')).encode('utf-8'))
	x_checksum = m2.hexdigest()
	x_header = {
		'X-Appid': x_appid,
		'X-CurTime': x_time,
		'X-CheckSum': x_checksum,
		'X-Param': x_param,
	}
	# 对图片一和图片二base64编码
	with open('./pic/'+str(id)+'.jpg', 'rb') as f:
		f1 = f.read()
	with open(r'./pic/temp.jpg', 'rb') as f:
		f2 = f.read()
	f1_base64 = str(base64.b64encode(f1), 'utf-8')
	f2_base64 = str(base64.b64encode(f2), 'utf-8')
	data = {
		'first_image': f1_base64,
		'second_image': f2_base64,
	}
	req = requests.post(url, data=data, headers=x_header)
	result = str(req.content, 'utf-8')
	print(result)  # 错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
	text='登录失败'
	if(result['data']>0.9):
		text='登录成功'
	tts(text)
	play_audio_file('res.wav')

	return



if __name__ == "__main__":
	app_movie()


    #app_joke()