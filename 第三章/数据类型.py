import random
# print(type("Hello"))
# print(type(10))
# print(type(3.14))
# print(type(True))
# # 判断数据类型
# num=10
# print(num)
# print(isinstance(num,int))#isinstance(数据，类型)
# s1="Hello"
# s2='Python'
# s3="""Hello:
#         欢迎光临
#         Python
#         """
# print(s1)
# print(s2)
# print(s3)
# s4='It\'s very good'#转义字符\'(单引号),\"(双引号),\n(换行),\t(tab键)
# print(s4)
# name="鳄鱼"
# age=18
# pro="计算机"
# hobby="Python"
# #str(int)将int类型的数字转化为字符串
# print("名字:"+name+",年龄:"+str(age)+",爱好:"+hobby)
# a=False
# b=not a
# c=(a and(b or not a))or a
# print(c)
# a=random.randint(1,100)
# b=random.uniform(1,100)
# c=random.random()
# print(a,b,c)
# s1="H"
# s2="O"
# oh=s2+s1
# hh=s1*2
# print(oh,hh)
# ohh=s2+s1*3
# print(ohh)
a=11
b=a%2
c=b==0
if c:
    print(a)
else:
    print(b)
