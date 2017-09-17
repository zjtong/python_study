__author__ = "zhanjintong"

with open("menu","r",encoding= "utf-8") as m:
    city = eval(m.read().strip() )

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