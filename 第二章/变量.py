# print(10)
# print(3.14)
# print(-5)
# print(True)
# print(False)
# print("Hello World")
# print("---------")
# print(None)
#
# for i in range(1,10):
#     for j in range(1,10):
#         if j<=i:
#             print(f"{j}×{i}={j*i}",end="\t")
#     print()
while True:
    username = input("用户名：")
    password = input("密码：")
    if username == "" or password == "":
        print("不能为空，重新输入")