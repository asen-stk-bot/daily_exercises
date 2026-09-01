# -*- coding: utf-8 -*-
"""练习(PPT第24页)：简单的用户登录系统
   用户名和密码必须与程序中保存的一致，直到登录成功或达到最大尝试次数
"""
SAVED_USERNAME = "admin"       # 程序中保存的正确用户名
SAVED_PASSWORD = "python123"   # 程序中保存的正确密码
MAX_TRIES = 3                  # 最大尝试次数

print("=== 用户登录系统 ===")
for attempt in range(1, MAX_TRIES + 1):
    username = input(f"[第{attempt}次] 请输入用户名: ")
    password = input(f"[第{attempt}次] 请输入密码: ")

    if username == SAVED_USERNAME and password == SAVED_PASSWORD:
        print(f"登录成功！欢迎你, {username}!")
        break
    else:
        remaining = MAX_TRIES - attempt
        if remaining > 0:
            print(f"用户名或密码错误！还有 {remaining} 次机会\n")
else:
    # for 循环没有被 break 时执行，即尝试次数用尽
    print("已达到最大尝试次数，账号锁定，登录失败！")
