__author__ = "zhanjintong"

city = {

    "广东":{
        "广州":{
            "白云区":"白云山",
            "荔湾区":["沙面","陈家祠"],
            "海珠区":"广州塔",
            "天河区":["广州塔","红砖厂创意园"],
            "越秀区":["石室圣心大教堂","越秀公园","五羊石像"]
                },
        "深圳":{
            "南山区":["世界之窗","欢乐谷","深圳大学"],
            "福田区":["红树林自然保护区"],
            "盐田区":["大梅沙海滨公园","东部华侨城"]
                },
        "肇庆":{
            "端州区":["七星岩","仙女湖","肇庆学院"],
            "鼎湖区":["鼎湖山","庆云寺"],
                }
            },

    "福建":{
        "厦门":{
            "思明区":["鼓浪屿","厦门大学","曾厝垵","中山路步行街"],
            "集美区":["集美学村","集美大学","集美鳌园"],
                },
        "福州":{
            "鼓楼区":["三坊七街","福州西湖公园","林则徐纪念馆"],
            "晋安区":["鼓山","福州国家森林公园"]
                },
        "泉州":{
            "鲤城区":["开元寺","清净寺"],
            "丰泽区":["清源山","西湖公园"]
                },
            },

    "广西":{
        "北海":{
            "海城区":"北海老街",
            "银海区":"北海银滩",
            "涠洲岛":["五彩滩","鳄鱼山火山公园","盛塘天主教堂"]
                },
        "南宁":{
            "西乡塘区":"广西大学",
            "青秀区":["青秀山","南湖公园","国际会展中心"]
                },
        "桂林":{
            "象山区":"象山公园",
            "雁山区":"漓江",
            "阳朔县":["西街","遇龙河","十里画廊"]
                }
            }
}

exit_flag = False
while not exit_flag :
    for c in city:
        print(c)
    choice1 = input("选择进入1-->")
    if choice1 in city:
        for c1 in city[choice1]:
            print("\t",c1)
    while not exit_flag:
        choice2 = input("选择进入2-->")
        if choice2 in city[choice1]:
            for c2 in city[choice1][choice2]:
                print("\t\t",c2)
        while not exit_flag:
            choice3 = input("选择进入3-->")
            if choice3 in city[choice1][choice2]:
                for c3 in city[choice1][choice2][choice3]:
                    print("\t\t\t",c3)
                choice4 = input("最后一层，按b返回上一层-->")
                if choice4 == "b":
                    pass
                elif choice4 == "q":
                    exit_flag = True

            if choice3 == "b":
                break
            elif choice3 == "q":
                exit_flag = True
        if choice2 == "b":
            break
        elif choice2 == "q":
            exit_flag =True