import snowboydecoder
import sys
import signal
from iat_ws import get_res
from sr_record import recording
from tts_ws import tts
from app_fun import *
import re
interrupted = False


def ctrl(a):
    pass
    #recording('ppp.pcm')
    cmd=get_res()
    fun_call(cmd)

def fun_map(cmd):
    if cmd=="讲个笑话。":
        return 0,{}
    elif cmd=="打开百度。":
        return 1,{}
    elif re.match("查询.+天气",cmd):
    	return 2,cmd.replace('查询','').replace('天气。','')
    elif cmd=="查询8787端口。":
    	return 3,'8787'
    elif cmd=="杀死8787端口进程。":
    	return 4,'8787'
    elif cmd=="123注册人脸。":
    	return 5,'123'
    elif cmd=="登录教务系统。":
    	return 6,{}
    elif cmd=="推荐一个电影。":
    	return 7,{}


    return -1,{}

def fun_call(cmd):
	ret,args=fun_map(cmd)
	if ret==0:
		app_joke()
	elif ret==1:
		app_baidu()
	elif ret==2:
		app_weather(args)
	elif ret==3:
		app_port(args)
	elif ret==4:
		app_kill_port(args)
	elif ret==5:
		app_reg_face(args)
	elif ret==6:
		app_whu_login()
	elif ret==7:
		app_movie()


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=snowboydecoder.play_audio_file,
               interrupt_check=interrupt_callback,
               audio_recorder_callback=ctrl,
               silent_count_threshold=5,
               sleep_time=0.03)

detector.terminate()
