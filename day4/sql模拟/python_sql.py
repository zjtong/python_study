#_*_coding:utf-8_*_
#第一部分:sql解析
import os
import linecache
def sql_parse(sql): #insert delete update select
    '''
    sql解析总控: 把sql字符串切分，提取命令信息，分发给具体的解析函数去解析
    :param sql:用户输入的字符串
    :return: 返回字典格式sql解析结果
    '''
    # insert into staff_table values Water,35,13910015353,teacher,2005-06-27
    # delete from staff_table where id=1
    # update staff_table set id=1 where name='alex'
    # select * from staff_table where not id= 1 and name = 'alex' or name= 'sb' limit 3
    parse_func={
        'insert':insert_parse,
        'delete':delete_parse,
        'update':update_parse,
        'select':select_parse,
    }
    sql_l=sql.split(' ')    #sql按空格切分，生成一个 list
    #print('sql_parse>>> ',sql_l)
    func=sql_l[0]
    res=''
    if func in parse_func:
        res=parse_func[func](sql_l)
    return res

def insert_parse(sql_l):
    # insert into staff_table values Water,35,13910015353,teacher,2005-06-27
    '''
    sql解析分支:insert
    :param sql_l: sql按照空格分割的列表
    :return: 返回字典格式的sql解析结果
    '''
    sql_dic={
        'func':insert, #函数名
        'insert':[],   #insert选项,留出扩展
        'into':[],     #表名
        'values':[],   #值
    }
    return handle_parse(sql_l,sql_dic)

def delete_parse(sql_l):
    # delete from staff_table where id=1
    '''
    sql解析分支:delete
    :param sql_l: sql按照空格分割的列表
    :return: 返回字典格式的sql解析结果
    '''
    sql_dic={
        'func':delete,
        'delete':[], #delete选项,留出扩展
        'from':[],   #表名
        'where':[],  #filter条件
    }
    return handle_parse(sql_l,sql_dic)

def update_parse(sql_l):
    # update staff_table set id=2 where name='alex'
    '''
    sql解析分支:update
    :param sql_l: sql按照空格分割的列表
    :return: 返回字典格式的sql解析结果
    '''
    sql_dic={
        'func':update,
        'update':[], #update选项,留出扩展
        'set':[],    #修改的值
        'where':[],  #filter条件
    }
    return handle_parse(sql_l,sql_dic)

def select_parse(sql_l):
    '''
    sql解析分支:select
    :param sql_l: sql按照空格分割的列表
    :return: 返回字典格式的sql解析结果
    '''
    #select name,age from staff_table where age > 22
    #select  * from staff_table where dept = "IT"
    #select  * from staff_table where enroll_date like "2013"
    sql_dic={
        'func':select,
        'select':[], #查询字段
        'from':[],   #表
        'where':[],  #filter条件
        'limit':[],  #limit条件
    }
    return handle_parse(sql_l,sql_dic)

def handle_parse(sql_l,sql_dic):
    '''
    填充sql_dic
    :param sql_l: sql按照空格分割的列表
    :param sql_dic: 待填充的字典
    :return: 返回字典格式的sql解析结果
    '''
    #select name,age from staff_table where age > 22
    #select  * from staff_table where dept = "IT"
    #select  * from staff_table where enroll_date like "2013"
    tag=False   #标志位
    for item in sql_l:
	    #['select', '', '*', 'from', 'text', 'where', 'id>', '4', 'and', '', 'id<', '', '', '', '10']
        #print(item)
        if item == "":continue  #清除空字符串: ''
        if item.startswith('\"') or item.endswith('\"') or item.startswith('\'') or item.endswith('\''):
            item = item.replace('\"',"")
            item = item.replace('\'', "")
        #item = item.lower()
        if tag and item in sql_dic:
            tag=False
        if not tag and item in sql_dic:
            tag=True
            key=item
            continue
        if tag:
            sql_dic[key].append(item)
    #print('before \033[33;1m%s\033[0m' %sql_dic)
    if sql_dic.get('where'):
        sql_dic['where']=where_parse(sql_dic.get('where'))
    #print('after \033[33;1m%s\033[0m' %sql_dic)
    #print('handle_parse>>> ',sql_dic )
    return sql_dic

def where_parse(where_l):
    '''
    对用户输入的where子句后的条件格式化,每个子条件都改成列表形式
    where_l: ['id>', '4', 'and', 'id<', '10'] --->  ['id', >', '4', 'and', 'id', '<', '10']
    :param where_l: 用户输入where后对应的过滤条件列表
    :return:
    '''
    res=[]
    key=['and','or','not']
    char=''
    #print('where_parse >>> ',where_l)
    for i in where_l:
        if i in key:
            if len(char) != 0:
                char=three_parse(char) #将每一个小的过滤条件如,id>=1转换成['id','>=','1']
                res.append(char)
            res.append(i)
            char=''
        else:
          char+=i
    else:
        char=three_parse(char)
        res.append(char)
    return res

def three_parse(exp_str):
    '''
    将每一个小的过滤条件如,id>=1转换成['id','>=','1']
    :param exp_str:条件表达式的字符串形式,例如'id>=1'
    :return:
    '''
    # print('three_opt before is \033[34;1m%s\033[0m' %exp_str)
    key=['>','=','<']   #逻辑运算符
    res=[]     #返回的列表
    char=''
    opt=''
    tag=False
    #exp_str = 'id>=1'
    for i in exp_str:
        if i in key:
            tag=True
            if len(char) !=0:
                res.append(char)
                char=''
            opt+=i
        if not tag:
            char+=i
        if tag and i not in key:
            tag=False
            res.append(opt)
            opt=''
            char+=i
    else:
        res.append(char)
    # print('res is %s ' %res)
    #新增like功能
    if len(res) == 1:#['namelike_ale5']
        res=res[0].split('like')    #str才可以split,res[0]是一个str
        res.insert(1,'like')
    return res







#第二部分:sql执行
def sql_action(sql_dic):
    '''
    执行sql的统一接口
    :param sql_dic:sql解析结果
    :return:
    '''
    return sql_dic.get('func')(sql_dic)

def insert(sql_dic):
    '''
    sql执行分支:insert，在文本最后插入
    :param sql_dic: sql解析结果
    :return: 返回字典格式的sql解析结果
    '''
    # insert into staff_table values Water,35,13910015353,teacher,2005-06-27
    print('insert %s' %sql_dic)
    table=sql_dic.get('into')[0]
    with open('%s' %table,'r+') as fh:
        linecount=len(fh.readlines())   #行数
        last = linecache.getline('%s' %table,linecount) #获取最后一行的数据
        last_id=int(last.split(',')[0])
        new_id=last_id+1    #id自增

        record=sql_dic.get('values')[0].split(',')
        record.insert(0,str(new_id))

        record_str=','.join(record)+'\n'
        #print(record_str )
        fh.write(record_str)
        fh.flush()
    return [['insert successful']]

def delete(sql_dic):
    #delete from staff_table where id=1
    table=sql_dic.get('from')[0]
    bak_file=table+'_bak'
    with open("%s" %table,'r',encoding='utf-8') as r_file,\
            open('%s' %bak_file,'w',encoding='utf-8') as w_file:
        del_count=0
        for line in r_file:
            title="id,name,age,phone,dept,enroll_date"
            dic=dict(zip(title.split(','),line.split(',')))
            filter_res=logic_action(dic,sql_dic.get('where'))
            if not filter_res:
                w_file.write(line)
            else:
                del_count+=1
        w_file.flush()
    os.remove("%s" %table)
    os.rename("%s" %bak_file,"%s" %table)
    return [[del_count],['delete successful']]

def update(sql_dic):
    #update staff_table set age=1 where id=1
    table=sql_dic.get('update')[0]
    set=sql_dic.get('set')[0].split(',')
    #print(type(set),set)
    set_l=[]
    for i in set:
        #print(i)
        if i.endswith('\"') or i.endswith('\''):
            i=i.replace('\"',"")
            i=i.replace('\'', "")
           # print(i)
        set_l.append(i.split('='))
    bak_file=table+'_bak'
    with open("%s" %table,'r',encoding='utf-8') as r_file,\
            open('%s' %bak_file,'w',encoding='utf-8') as w_file:
        update_count=0
        for line in r_file:
            title="id,name,age,phone,dept,enroll_date"
            dic=dict(zip(title.split(','),line.split(',')))
            filter_res=logic_action(dic,sql_dic.get('where'))
            if filter_res:
                #print(filter_res )
                for i in set_l:
                    k=i[0]
                    v=i[-1].strip(",")
                    #print('k v %s %s' %(k,v))
                    dic[k]=v
                print('change dic is %s ' %dic)
                line=[]
                for i in title.split(','):
                    line.append(dic[i])
                update_count+=1
                line=','.join(line)
            w_file.write(line)

        w_file.flush()
    os.remove("%s" % table)
    os.rename("%s" %bak_file,"%s" %table)
    return [[update_count],['update successful']]

def select(sql_dic):
    '''
    sql执行分支:select
    :param sql_dic: 字典格式的sql解析结果
    :return: 返回字典格式的sql解析结果
    '''

    # select * from staff_table where not id= 1 and name = 'alex' or name= 'sb' limit 3
    #first : from
    table=sql_dic.get('from')[0]
    fh=open("%s" %table,'r',encoding='utf-8')
    #second : where
    where_res=where_action(fh,sql_dic.get('where'))
    fh.close()
    #third : limit
    limit_res=limit_action(where_res,sql_dic.get('limit'))
    #fourth
    search_res=search_action(limit_res,sql_dic.get('select'))

    return search_res

def where_action(fh,where_l):
    #print(where_l )
    res=[]
    logic_l=['and','or','not']
    title="id,name,age,phone,dept,enroll_date"
    if len(where_l) !=0:
        for line in fh:
            #line = line.strip().lower()     #都变成小写字母 >>> 输入不区分大小写
            line = line.replace(" ","") #去掉空格
            #print(line)
            dic=dict(zip(title.split(','),line.split(',')))
            #print(dict)
            logic_res=logic_action(dic,where_l)
            if logic_res:
                res.append(line.split(','))
    else:
        res=fh.readlines()
    return res

def logic_action(dic,where_l):
    #print(dic,where_l)
    #逻辑运算
    res=[]
    # print('==\033[45;1m%s\033[0m==\033[48;1m%s\033[0m' %(dic,where_l))
    for exp in where_l:
        #where_l  [['age', '>', '22'],['dept','=','IT']
        #dic {'name': 'Alex Li', 'phone': '13651054608', 'id': '1', 'dept': 'IT', 'age': '22', 'enroll_date': '2013-04-01'}
        #exp = exp.strip('\\"\\')
        #print(exp)
        if type(exp) is list:
            exp_k,opt,exp_v=exp
            #exp_v = exp_v.strip('\\"\\')
            #print("exp_v : ",exp_v )
            if exp[1] == '=':
                opt='%s=' %exp[1]
            if dic[exp_k].isdigit():
                dic_v=int(dic[exp_k])
                exp_v=int(exp_v)
            else:
                dic_v="%s" %dic[exp_k]
            if opt != 'like':
                exp=str(eval("'%s'%s'%s'" %(dic_v,opt,exp_v)))
            else:
                if exp_v in dic_v:
                    exp='True'
                else:
                    exp='False'
        res.append(exp)
    res=eval(' '.join(res))
    # print('==\033[45;1m%s\033[0m' %(res))
    return res

def limit_action(filter_res,limit_l):
    #limit 3
    res=[]
    if len(limit_l) !=0:    #limit_l 限制条件
        index=int(limit_l[0])
        res=filter_res[0:index] #切片
    else:   #没有限制条件
        res=filter_res
    return res

def search_action(limit_res,select_l):
    # select id,name from staff_table where not id= 1 and name = 'alex' or name= 'sb' limit 3
    res=[]
    fileds_l=[]
    title="id,name,age,phone,dept,enroll_date"
    if select_l[0] == '*':
        res=limit_res
        fileds_l=title.split(',')
    else:

        for record in limit_res:
            dic=dict(zip(title.split(','),record))
            # print("dic is %s " %dic)
            fileds_l=select_l[0].split(',')
            r_l=[]
            for i in fileds_l:
                r_l.append(dic[i].strip())
            res.append(r_l)

    return [fileds_l,res]



if __name__ == '__main__':
    while True:
        sql=input("sql> ").strip()
        if sql == 'exit':break
        if len(sql) == 0:continue

        sql_dic=sql_parse(sql)

        if len(sql_dic) == 0:continue
        res=sql_action(sql_dic)

        for i in res[-1]:
            print(i)