__author__ = 'ZJT'

def read_in_dic(filename):
	"""从文件读取文本数据并转成字典形式"""
	with open("%s"%filename,"r",encoding= "utf-8") as f:
		item_dic = {}
		for item in f:
			item_dic.update(eval(item))
	return item_dic
def write_in_dic(filename,object):
	"""把变量object写入文本中"""
	with open("%s"%filename,"a",encoding= "utf-8") as f:
		f.write("%s\n"%object)



count = 1
user = {}
shopping_list = []
record = {}
exit_flag = False
recharge_flag = False	#充值标志，通过置0置1来选择充值的功能


while True:
	'''判断用户是不是第一次登录？
		是>>>读取用户数据并赋值给user,询问是否查询消费记录
		不是>>>把当前用户数据赋值给user,salary = 0
	'''
	while not exit_flag :
		#print(count)
		username = input("请输入你的用户名:")
		password = input("请输入你的密码:")
		users = read_in_dic("users")
		#print(users)
		if username in users:
			if password == users[username][0]:
				user[username] = [users[username][0],users[username][1]]
				salary = user[username][1]

				"""查询消费记录？"""
				choice = input("查询消费记录？y or n>>>")
				if choice != "n" :
					print("\033[32;1m 消费记录 \033[0m".center(50,"-") )
					with open("records","r",encoding= "utf-8") as r:
						for r_item in r:
							if username in eval(r_item):		#输入的用户名有记录，把记录添加到字典records
								print("{_count}:\t{_record}".format(_count = count,_record =eval(r_item)[username ]) )
								count+=1
					print("\n")
				exit_flag = True
			else:
				count+=1
				print("密码错误！密码输错3次将自动退出！")
				print("您已输错%s次...\n"%(count-1))

				if count > 3:
					exit()
		else:
			user[username] = [password,0]
			salary = user[username][1]
			recharge_flag  = True
			exit_flag = True
	#print(user)

	"""充值金额"""
	while  recharge_flag :
		recharge_salary = input("输入你的充值金额：")
		if recharge_salary.isdigit():
			recharge_salary = int(recharge_salary)
			salary +=recharge_salary
			recharge_flag  = False
		else:
			print("\t\t请输入数值！")

	products = read_in_dic("products")
	products_list = list(products.values())
	for index,item in enumerate(products_list) :	#打印商品列表
		print(index ,item )

	print("您的余额为\033[31;1m %s \033[0m："%salary)

	number = input("输入你要购买的商品编号：")
	if number.isdigit():
		number = int(number )
		if number >= 0 and number < len(products_list ):
			if salary >= products_list[number][1]:
				salary -= products_list[number][1]
				shopping_list.append(products_list[number])
			else:
				print("\033[41;1m金额不足，无法购买！ \033[0m")
				choice1 = input("是否充值？ y or n >>>")
				if choice1 != "n":
					recharge_flag = True
		else:
			print("输入编号错误，商品不存在！")
	elif number == "q":
		print("\033[32;1m 购物清单 \033[0m".center(50,"-") )
		for s_item in shopping_list :
			print("\033[31;1m %s \033[0m"%s_item)

		record["%s"%username] = shopping_list 						#购物记录-用户名，记录，以字典形式存储
		write_in_dic("records",record)

		user["%s"%username] = [password	,salary]				#用户信息-用户名、密码、余额
		write_in_dic("users",user)
		break
	else:
		print("请输入数值！")

