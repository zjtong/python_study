__author__ = 'ZJT'
#_*_ encoding=utf-8 _*_

def fetch(data):

	"""获取data对应的backend的server信息"""
	"""
	backend www.oldboy.org
        server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000
        server 100.1.7.8 100.1.7.9 weight 20 maxconn 3000
	backend www.oldboy.com
        server 100.1.7.8 100.1.7.9 weight 20 maxconn 3000
    """
	backend = "backend %s"%data
	server_list = []		#服务信息列表
	find_flag = False		#标志位，找到置1,没找到置0
	with open("haproxy","r",encoding="utf-8") as f:
		for line in f:				#遍历
			if backend == line.strip() :		#匹配
				find_flag = True	#匹配到>>>标志位置1
				continue			#重新开始下一行

			if find_flag and line.startswith("backend") :		#不是以"server"开头的，则把标志位置0
				find_flag = False
			if find_flag and line:		#把内容添加到服务信息列表
				server_list .append(line.strip())
	return server_list

def add(data):
	"""1:添加的内容已存在；部分存在&全部存在，2：添加的内容不存在"""
	"""data ={'bakend': 'www.oldboy.org','record':{'server': '100.1.7.9','weight': 20,'maxconn': 30}}"""
	'''判断添加的内容存不存在'''
	add_backend ="backend %s"%data.get("backend")
		#要添加的内容的backend,字典的get()>>有就返回对于的值，没有返回None，直接data["backend"]取值时，当用户输入错误
		# 容易报字典键不存在的错误，使程序直接停止
	server_list = fetch(data.get("backend"))				#通过fetch（）查找要添加的内容是否存在，存在就添加到server_list中
	add_server = "server %s %s weight %d maxconn %d"%(data["record"]["server"],\
													  data["record"]["server"],\
													  data["record"]["weight"],\
													  data["record"]["maxconn"])
	if not server_list:		#server_list 为空时执行,即要添加的内容在文件里不存在
		"""backend与server在文件中都不存在"""
		server_list.append(add_backend )
		server_list.append(add_server )
		with open("haproxy","r") as read_file,\
				open("haproxy_new","w") as write_file:
			for line in read_file:			#逐行读取、逐行写入
				write_file.write(line)

			for item in server_list :		#在最后添加用户要增加的内容
				if item.startswith("backend"):
					write_file .write("%s\n"%item)
				else:
					write_file .write("%s%s\n"%(" "*8,item))
	else:			#要添加的内容在文件里存在
		"""backend与server在文件中都存在"""
		"""server 与文件中的相同"""
		if add_server  in server_list :
			print("添加的内容已存在")


		else:
			"""用户输入的server 与文件中的不相同"""
			server_list .insert(0,add_backend )
			server_list .append(add_server)
			"""现在的 server_list 存放的的时原文件中的backend 与 server 信息"""
			with open("haproxy", "r") as read_file, \
				open("haproxy_new", "w") as write_file:

				find_flag = False
				finish_flag = False
				for line in read_file:
					if line.strip() == add_backend:
						find_flag = True
						continue
					if find_flag and line.startswith("backend"):
						find_flag = False

					if not find_flag:
						write_file.write(line)
					else:
						if not finish_flag:
							for item in server_list:
								if item.startswith('backend'):
									write_file.write(item + '\n')
								else:
									write_file.write("%s%s\n" % (8 * " ", item))
						finish_flag = True

def remove(data):
	del_backend = "backend %s" % data.get("backend")
	# 要添加的内容的backend,字典的get()>>有就返回对于的值，没有返回None，直接data["backend"]取值时，当用户输入错误
	# 容易报字典键不存在的错误，使程序直接停止
	"""data ={'bakend': 'www.oldboy.org','record':{'server': '100.1.7.9','weight': 20,'maxconn': 30}}"""
	server_list = fetch(data.get("backend"))  # 通过fetch（）查找要删除的内容是否存在，存在就添加到server_list中
	del_record = "server %s %s weight %d maxconn %d" % (data["record"]["server"], data["record"]["server"], \
														data["record"]["weight"], data["record"]["maxconn"])

	if not server_list or del_record not in server_list :
		#server_list为空时执行，即想删除的内容在文件里不存在
		# 文件中的server信息与要删除的server信息不同,即要删除的server信息不存在
		print("删除的内容不存在")
		return


	else:			#要删除的server信息存在
		del server_list [server_list .index(del_record )]	#从文件读取的server信息列表删除掉要删除的内容
		"""现在的 server_list 存放的的时原文件中的 server 信息"""
		if server_list :		#删除后server列表不为空时执行，即server列表里还有内容，要把它写到新文件里
			server_list .insert(0,del_backend)
			"""现在的 server_list 存放的的时原文件中的backend 与 server 信息"""
			del_flag = True		#删除的内容和文件中的内容不相同，有一些不能删除
		else:
			del_flag = False		#删除的内容和文件中的内容相同，直接删除所有的内容

		find_flag = False
		with open("haproxy","r") as read_file,\
			open("haproxy_new","w") as write_file:

				if  del_flag :	#删除的内容和文件中的内容不相同，有一些不能删除
					finish_flag = False
					for line in read_file:
						if line.strip()  == del_backend :
							find_flag = True
							continue
						if find_flag and line.startswith("backend"):
							find_flag = False

						if not find_flag:
							write_file .write(line)
						else:
							if not finish_flag :
								for item in server_list :
									if item.startswith('backend'):
										write_file.write(item +'\n')
									else:
										write_file.write("%s%s\n" % (8*" ", item))
							finish_flag = True

				else:					#删除的内容和文件中的内容相同，直接删除所有的内容
					for line in read_file:
						if line.strip()  == del_backend :
							find_flag = True
							continue
						if find_flag and line.startswith("backend"):
							find_flag = False
						if not find_flag:
							write_file .write(line)



if __name__ == "__main__":
	function="""
		1:查询
		2:添加
		3:删除
		4:退出"""
	func_dic = {
		"1":fetch,
		"2":add,
		"3":remove,
		"4":exit
	}

while True:
	print(function)
	choice = input("选择>>>:").strip()
	if len(choice) == 0 or choice not in func_dic: continue
	if choice == "4": break
	data = input("数据>>>:").strip()
	if len(data) == 0 :continue
	if data == "q":break
	if choice != "1":
		data = eval(data)
	func_dic[choice](data)
	if choice == "1":
		list = func_dic[choice](data)
		for item in list:
			print(item)
