__author__ = "zjt"

import re

def multiply_and_divide(formula):
	"""计算乘法与除法"""
	exit_flag = False
	while not exit_flag :
		# 匹配乘法或者除法算式
		get_formula = re.search(r'\d+\.?\d*[\*\/]\-?\d+\.?\d*',formula )
		if get_formula :
			get_formula = get_formula .group()
			#print(get_formula )
			if "*" in get_formula:
				calc_list = get_formula .split("*")
				result = float(calc_list [0]) * float(calc_list [1])
				formula = formula .replace(get_formula,str(result))
			elif '/' in get_formula:
				calc_list = get_formula.split('/')
				result = float(calc_list[0]) / float(calc_list[1])
				formula = formula.replace(get_formula, str(result))
			else:
				result = get_formula
				#continue
		else:
			exit_flag = True
	return formula

def add_and_sub(formula):
	'''计算加减'''
	exit_flag = False
	while not exit_flag :
		formula = formula.strip()
		get_formula = re.search(r'\-?\d+\.?\d*[\+\-]\-?\d+\.?\d*',formula )
		if get_formula :
			get_formula = get_formula .group()
			#print(get_formula )
			if "+" in get_formula:
				calc_list = get_formula .split("+")
				result = float(calc_list [0]) + float(calc_list [1])
				formula = formula .replace(get_formula,str(result))
			elif '-' in get_formula:
				calc_list = get_formula.split('-')
				#print(calc_list)
				if calc_list [0] == "" :	# -a 或者 -a-b
					if len(calc_list) == 2:	# -a
						exit_flag = True
					else:					# -a-b
						result = float("-%s" % (calc_list[1])) - float(calc_list[2])
						formula = formula.replace(get_formula, str(result))
				else:
					result = float(calc_list [0]) - float(calc_list[1])
					formula = formula.replace(get_formula, str(result))
			else:
				result = get_formula
				#continue
		else:
			exit_flag = True
	#print(result)
	return formula

def remove_symbols(formula):
	"""去掉重复的符号"""
	formula = formula.strip()
	formula = formula.replace("++", "+")
	formula = formula.replace("+-", "-")
	formula = formula.replace("-+", "-")
	formula = formula.replace("--", "+")
	return formula

def compute(formula):
	'''这里计算是的不带括号的公式'''
	# (2+3+2/4)

	formula = formula.strip("()")  # 去除外面包的拓号

	exit_flag = False
	while not exit_flag :

		#print(formula)
		if "*" in formula or "/" in formula :
			formula = multiply_and_divide(formula )
		elif "+" in formula or "-" in formula:
			formula = remove_symbols(formula)  # 去除外重复的+-号
			if "+" in formula:
				formula = add_and_sub(formula)
			else:

				m = formula.split("-")	# -a 或 -a-b(-a+b)
				#print(m)
				if m[0] == "":
					if len(m) == 2:		# -a
						exit_flag = True
					else:
						formula = add_and_sub(formula)
				else:
					formula = add_and_sub(formula)
		else:
			exit_flag = True
	return formula

def calc(formula):
	'''计算程序主入口, 主要逻辑是先计算拓号里的值,算出来后再算乘除,再算加减'''
	formula = re.sub(r"\ ","",formula)
	parenthesise_flag = True
	while parenthesise_flag:
		get_formula  = re.search("\([^()]*\)", formula)  # 找到最里层的拓号
		if get_formula:
			# print("先算拓号里的值:",m.group())
			result = compute(get_formula.group())
			formula = formula.replace(get_formula.group(), str(result ))
		else:
			#print('\033[41;1m----没拓号了...---\033[0m')

			print('\n\033[32;1m最终结果:\033[0m', compute(formula))
			parenthesise_flag = False  # 代表公式里的拓号已经都被剥除啦


if __name__ == '__main__':
	formula = input('请输入算式：')
	#formula = " 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"
	calc(formula)



