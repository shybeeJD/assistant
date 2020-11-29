import os



def app_port(num):
	cmd='sudo lsof -i:'+num
	res=os.popen(cmd,'w').write('   ')
	output=res.readlines()
	ret=[]
	if output:
		for item in output[1:]:
			print(item)
			item=item.strip().split()
			ret.append([item[0],item[1]])

	print(ret)
	return ret

def app_kill_port(num):
	cmd="kill -"


if __name__ == "__main__":
	app_port('8787')

