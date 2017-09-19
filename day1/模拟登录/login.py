__author__ = 'Administrator'

normal_users = {}
lock_users = {}
count = 0
while count<3:
	username = input("请输入你的用户名:")
	password = input("请输入你的密码:")

	'''  read normal_users from file:normal_users  '''
	with open("normal_users", "r+", encoding=("utf-8")) as f:
		for normal_user in f:
			a = normal_user.strip().split("&")
			normal_users[a[0]] = a[1]
	#print("normal_users: ", normal_users)

	'''  read lock_users from file:lock_users  '''
	with open("lock_users", "r+", encoding=("utf-8")) as f1:
		for lock_user in f1:
			b = lock_user.strip().split("&")
			lock_users[b[0]] = b[1]
	#print("lock_users: ", lock_users)

	if username in lock_users :		#判断用户名是否被锁定
		print("你的用户名被锁定！")
		break

	elif username not in normal_users :		#判断用户名是否存在
		print("你输入的用户名不存在...")
		choice = input("\t是否注册新用户？y or n>>>")
		if choice == "y":
			new_username = input("注册的用户名为：")
			new_password = input("注册的密码为：")
			print("\n")
			with open("normal_users", "a", encoding=("utf-8")) as f2:
				f2.write("{name}&{word}\n".format(name=new_username ,word=new_password ) )
		elif choice == "n":
			continue


	else :		#用户名没有被锁定，不是不存在
		if password == normal_users[username]:
			print("欢迎用户[%s]登录！" % username)
			break
		else:
			print('''密码错误，请重新输入...
			输错3次该用户名将被锁定，你已经输错[%s]次''' % (count + 1))
		count += 1

else:
	print("密码输入错误3次你的用户名被锁定！")
	with open("lock_users","a",encoding="utf-8") as f:
		f.write("{name}&{word}\n".format(name=username,word=password))
